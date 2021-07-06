#import main.generator as gen
#import main.reader as reader
import pandas as pd
from pandas.core.dtypes.missing import notna
import main.writer.DML as writer


def main(insert, data=None, trail=None, update=False, order=1, CourseTrailOrder=1, env='hml'):
    """
        insert : {'trail', 'course', 'module', 'lecture', 'product', 'coursetrail', 'article', 'file'}

    """
    if insert=='trail':
        result = writer.insert_trail( 'Trail',
            title='Educação financeira e finanças pessoais',
            description='Educação financeira é uma ferramenta essencial para alcançar uma vida mais tranquila e estável. Nesta trilha, você aprende sobre educação financeira e finanças pessoais de forma prática, clara e direta.',
            backgroundUrlBanner='',
            backgroundUrlDesktop='https://tc.com.br/wp-content/uploads/2021/05/thumb_educaca_financeira.png',
            backgroundUrlMobile='https://tc.com.br/wp-content/uploads/2021/05/thumb_educaca_financeira.png'
        )
    elif insert=='course':
        result = writer.insert_course( 'Course',
            productId=62,
            title='Ondas de Elliott: entenda os segredos dos gráficos', 
            objective='Tudo o que você precisa saber sobre as Ondas de Elliott: desde a teoria que envolve as ondas até as aplicações práticas com análises de exemplos reais.', 
            certification=None,
            certificationActive=0, 
            targetAudience=None, 
            workload=None, 
            timeAvailable=None, 
            topics=None, 
            backgroundUrl='https://tc.com.br/wp-content/uploads/2021/06/thumb-elliott.png',
            sequential=1, 
            categoryId='5db1a95f0b19960058b9e188', 
            published=1,
            subscriptionsCount=0, 
            active=1, 
            dropoutPercentage=110.00, 
            isOpenCourse=0, 
            imgMobileUrl='https://tc.com.br/wp-content/uploads/2021/06/banner_mobile-elliott.png',#TODO
            imgBannerUrl='https://tc.com.br/wp-content/uploads/2021/06/banner-web-elliott.png'#TODO

        )
    elif insert=='module':
        titles = dict()
        for i in range(data.shape[0]):
            if data['Número Módulo'].iloc[i] not in titles.keys():
                titles[ data['Número Módulo'].iloc[i] ] = data['Nome Módulo'].iloc[i]
        for i in titles.keys():
            result = writer.insert_module(
                id=None, 
                title=titles[i], 
                order=i, 
                courseId=None,
                courseName=data['Curso'].loc[0],
                active=1, 
                activeTest=1
            )

    elif insert=='lecture':
        last_module = None
        for i in range(data.shape[0]):
            if pd.isna(data['Vimeo ID'].iloc[i]):
                continue
            
            result = writer.insert_lecture(
                ModuleName=data['Nome Módulo'].iloc[i], 
                CourseName=data['Curso'].iloc[i], 
                Tittle=data['Nome Aula'].iloc[i], 
                Order=data['Número Aula'].iloc[i], 
                VideoId=data['Vimeo ID'].iloc[i].split('/')[-1], 
                Active=1,
                VideoDuration=data['Tempo Vídeo'].iloc[i] if pd.notna(data['Tempo Vídeo'].iloc[i]) else None,
                IsBonus=1
                )
            print(result)
            
    elif insert == 'product':
        result = writer.insert_product(Title=data['Curso'].loc[0])

    elif insert == 'coursetrail':
        result = writer.insert_coursetrail(
            CourseName=data['Curso'].loc[0],
            TrailName=trail,
            CourseTrailOrder=1
        )
    elif insert == 'article':
        for i in range(data.shape[0]):
            if pd.isna(data['Artigo'].iloc[i]) or data['Artigo'].iloc[i] == '':
                continue
            if i==0 or data['Nome Aula'].iloc[i-1]!=data['Nome Aula'].iloc[i]:
                order = 1
            elif pd.isna(data['Artigo'].iloc[i-1]) or data['Artigo'].iloc[i-1] == '':
                order = 1
            else:
                order += 1
            result = writer.insert_article(
                LectureName=data['Nome Aula'].iloc[i],
                ModuleName=data['Nome Módulo'].iloc[i], 
                CourseName=data['Curso'].loc[0], 
                Title= data['Artigo'].iloc[i], 
                WordpressUrl=data['Link Artigo'].iloc[i],
                Order=order
            )
            print(result)
    
    elif insert == 'file':                
        result = writer.file_get_infos(data)

    return result

import main.generator.go_interface as go

print(go.go_get_id())


exit(1)


insert='article' #{'trail', 'course', 'module', 'lecture', 'product', 'coursetrail', 'article', 'file'}
env = 'hml'

trail = ''
CourseTrailOrder=4

name = 'Aulas ao vivo - USO SQUAD.csv'
data = pd.read_csv(f'~/Downloads/TCSchool - files/{name}') if insert not in {'trail', 'course'} else None

result = main(insert, data=data, trail=trail, update=True, order=10, CourseTrailOrder=CourseTrailOrder, env=env)
print(result)
