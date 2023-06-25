from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
app = FastAPI()
#http://127.0.0.1:8000
@app.get('/')
async def read_root():
   return {'api proyecto individual'}

@app.on_event("startup")
async def load_data():
   global df, df_actores,df_fdir_csv,tfidf,tfidf_matrix,df_recomendacion,cosine_sim,indices
   
   df =pd.read_csv('data_output/df_movies_api.csv',sep=',',encoding='latin1')
   df_actores = pd.read_csv('data_output/df_actor.csv',sep=';',encoding='latin1')
   df_fdir_csv = pd.read_csv('data_output/df_fdirector_cs.csv',encoding='latin1')
   df_recomendacion = pd.read_csv('data_output/df_recomendacion.csv',encoding='latin1')
   # recomendacion
   tfidf = TfidfVectorizer(stop_words='english',max_features=5000)
   tfidf_matrix =tfidf.fit_transform(df_recomendacion['noverviwe'])
   cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
   indices = pd.Series(df_recomendacion.index, index=df_recomendacion['title'])


@app.get('/cantidad_filmaciones_mes/({mes})')
def cantidad_filmaciones_mes(mes:str):
  '''Se ingresa el mes y la funcion retorna lacantidad de peliculas 
     que se estrenaron ese mes historicamente. '''
  index_u = df[['index','release_month']].drop_duplicates()
  serie = index_u.groupby('release_month').count()['index']
  mes = mes.capitalize()
  respuesta = int(serie[mes])
  return {'mes':mes,'cantidad peliculas mes':respuesta}

@app.get('/cantidad_filmaciones_dia/({dia})')
def cantidad_filmaciones_dia(dia:str):
   '''Se ingresa el dia y la funcion retorna la cantidad de peliculas 
      que se estrenaron ese dia historicamente.'''

   index_u = df[['index','release_day']].drop_duplicates()
   serie= index_u.groupby('release_day').count()['index']
   dia = dia.capitalize()
   respuesta = int(serie[dia])
   return {'dia':dia,'cantidad peliculas dia':respuesta}

@app.get('/score_titulo/({titulo})')
def score_titulo(titulo:str):
  '''Se ingresa el titulo de una filmacion y la funcion retorna
     el titulo, el año de estreno y el score.'''

  index_u = df[['index','release_year','title','popularity']].drop_duplicates()
  ind_2 =index_u.set_index('title',drop=False)
  title = str(ind_2.loc[titulo][2])
  year = int(ind_2.loc[titulo][1])
  popul = int(ind_2.loc[titulo][3])
  return {'title':title, 'year':year, 'popularidad':popul}

@app.get('/votos_titulo/({titulo})')
def votos_titulo(titulo:str):
  '''Se ingresa titulo de filmacion y la funcion retorna titulo, cantidad de votos 
     valor promedio de votos, si los votos totales son menores a 2000 no se mostraran
     resultados.'''
  unicos = df[['title','vote_count','vote_average']].drop_duplicates()
  unicos_2 = unicos.set_index('title',drop=False)
  title = str(unicos_2.loc[titulo][0])
  vote = int(unicos_2.loc[titulo][1])
  v_aver = round(float(unicos_2.loc[titulo][2]),2)
  if vote >= 2000:
    return {'titulo':title,'voto_total':vote,'voto_promedio':v_aver}
  else:
    return {'votos':'La pelicula no cuenta con mas de 2000 votos'}
  
@app.get('/get_actor/({nombre_actor})')
def get_actor(nombre_actor:str):
  '''Se ingresa el nombre de un actor y la funcion retorna el exito
     medido a través del retorno, tambien devuelve la cantidad de peliculas,
     y el promedio del retorno.'''
  total_retorno_actor = df_actores.groupby('castdos').sum()['return']
  t_r_a = round(float(total_retorno_actor[nombre_actor]),2)
  promedio_retorno_actor = df_actores.groupby('castdos').mean()['return']
  p_r_a= round(float(promedio_retorno_actor[nombre_actor]),2)
  total_peliculas_actor = df_actores.groupby('castdos').count()['id']
  t_p_a = int(total_peliculas_actor[nombre_actor])
  return  {'actor':nombre_actor,'cantidad filmaciones':t_p_a,'retorno_total':t_r_a,'retorno_promedio':p_r_a}

@app.get('/get_director/({nombre_director})')
def get_director(nombre_director:str):
  
  '''Se ingresa el nombre de un director y la función retorna el éxito del mismo medido a través
  del retorno, también retorna una lista con la peliculas, año de lanzamiento, retorno, costo y
  ganancia de cada pelicula.
  '''
  
  retorno_director = df_fdir_csv.groupby('crewdos').sum()['return']
  r_t_d = round(float(retorno_director[nombre_director]),2)
  datos_director = df_fdir_csv[df_fdir_csv['crewdos']==nombre_director]
  pelis = list(datos_director['title'])
  release = list(datos_director['year'])
  retorno = list(datos_director['return'])
  budget = list(datos_director['budget'])
  revenue = list(datos_director['revenue'])
  
  return {'director':nombre_director,'retorno_dir':r_t_d,'peliculas':pelis,'release_year':release,
          'retorno':retorno,'budget':budget,'revenue':revenue}

@app.get('/recomendacion/({title})')
def recomendacion(title:str):
  '''Se ingresa el nombre de una pelicula y la funcion arroja una lista con cinco 
  peliculas recomendadas.'''     
       
  idx= indices[title]
  sim_scores = list(enumerate(cosine_sim[idx]))
  sim_scores=sorted(sim_scores,key=lambda x: x[1],reverse =True)
  sim_scores = sim_scores[1:6]
  movie_indices = [i[0] for i in sim_scores]
  respuesta = list(df_recomendacion['title'].iloc[movie_indices])
  return {'lista cinco peliculas recomendadas': respuesta}



