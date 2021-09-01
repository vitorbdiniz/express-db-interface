#import main.generator as gen
#import main.reader as reader
import pandas as pd
from pandas.core.dtypes.missing import notna
import main.writer.DML as writer


def main(insert, data=None, trail=None, update=False, order=1, productId=None, CourseTrailOrder=1, env='hml'):
    """
        insert : {'trail', 'course', 'module', 'lecture', 'product', 'coursetrail', 'article', 'file'}

    """
    result = None
    if insert=='trail':
        result = writer.insert_trail( 'Trail',
            title='Renda Fixa',
            description='Os investimentos de renda fixa ainda são os preferidos de muitos investidores. Nesta trilha, são apresentados cursos que abordam os principais conceitos da renda fixa, os diferentes tipos de investimentos, como analisar e muita aplicação prática.',
            backgroundUrlBanner='',
            backgroundUrlDesktop='',
            backgroundUrlMobile=''
        )
    elif insert=='course':
        result = writer.insert_course( 'Course',
            productId=productId,
            title=data['Curso'].iloc[0], 
            objective='Neste curso nós apresentamos uma introdução às finanças descentralizadas e te mostramos como utilizar os principais protocolos utilizando a carteira Web 3.0 MetaMask.', 
            certification=None,
            certificationActive=0,
            targetAudience=None, 
            workload=None, 
            timeAvailable=None, 
            topics=None, 
            backgroundUrl='https://tc.com.br/wp-content/uploads/2021/07/defi_thumb.png',
            sequential=1, 
            categoryId='5db1a95f0b19960058b9e188', 
            published=1,
            subscriptionsCount=0, 
            active=1, 
            dropoutPercentage=110.00, 
            isOpenCourse=0,
            imgMobileUrl='https://tc.com.br/wp-content/uploads/2021/07/defi_banner_mobile.png',
            imgBannerUrl='https://tc.com.br/wp-content/uploads/2021/07/defi_banner_web.png',
            courseSlug=None,
            LearningLevelId= 'Intermediário'

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
            print(titles[i])

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
                IsBonus=data['Bonus'].iloc[i] if pd.notna(data['Bonus'].iloc[i]) else 0
                )
            print(data['Nome Aula'].iloc[i])
            
    elif insert == 'product':
        result = writer.insert_product(Title=data['Curso'].loc[0])

    elif insert == 'coursetrail':
        result = writer.insert_coursetrail(
            CourseName=data['Curso'].loc[0],
            TrailName=trail,
            CourseTrailOrder=CourseTrailOrder
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
    elif insert == 'refference':
        if (pd.notna(data['Link Referência'])).any():
            for i in range(data.shape[0]):
                if pd.isna(data['Link Referência'].iloc[i]) or data['Link Referência'].iloc[i] == '':
                    continue
                if i==0 or data['Nome Aula'].iloc[i-1]!=data['Nome Aula'].iloc[i]:
                    order = 1
                elif pd.isna(data['Link Referência'].iloc[i-1]) or data['Link Referência'].iloc[i-1] == '':
                    order = 1
                else:
                    order += 1

                result = writer.insert_refference(
                    LectureName=data['Nome Aula'].iloc[i],
                    ModuleName=data['Nome Módulo'].iloc[i], 
                    CourseName=data['Curso'].loc[0], 
                    ReffUrl=data['Link Referência'].iloc[i], 
                    Order=order,
                    Title=data['Nome Link Referência'].iloc[i],
                    Description=''
                )

    elif insert == 'file':                
        result = writer.file_get_infos(data)


    print(f'-> {insert} Insert OK')
    return result





#get_inserts = lambda insert_all, item=[] : ['course', 'module', 'lecture', 'product', 'coursetrail', 'article', 'refference','file'] if insert_all else item #'trail'
get_inserts = lambda insert_all, item=[] : ['course', 'module', 'lecture', 'product', 'article', 'refference','file'] if insert_all else item #'trail'

insert_all = True
item = ['file'] if not insert_all else []

env = 'hml'

trail = ''
CourseTrailOrder=1
productId = 69
turmas = [1,2]

name = 'defi.csv'
data = pd.read_csv(f'~/Downloads/TCSchool - files/{name}')

for insert in get_inserts( insert_all, item ):
    if 'experience.csv' == name:
        for turma in turmas:
            data = pd.read_csv(f'~/Downloads/TCSchool - files/{name}') if insert not in {'trail'} else None
            productId += turma
            data['Curso'] += f' - Turma {turma}'
            result = main(insert, data=data, trail=trail, update=True, order=10, productId=productId, CourseTrailOrder=CourseTrailOrder, env=env)
    else:
        result = main(insert, data=data, trail=trail, update=True, order=10, productId=productId, CourseTrailOrder=CourseTrailOrder, env=env)



