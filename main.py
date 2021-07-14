#import main.generator as gen
#import main.reader as reader
import pandas as pd
from pandas.core.dtypes.missing import notna
import main.writer.DML as writer


def main(insert, data=None, trail=None, update=False, order=1, productId=None, CourseTrailOrder=1, env='hml'):
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
            productId=productId,
            title=data['Curso'].iloc[0], 
            objective='Há diversos investimentos com diferentes características disponíveis no mercado. Neste curso você aprende sobre os principais tipos e a como escolher os investimentos ideais para o seu objetivo de vida.', 
            certification=None,
            certificationActive=0, 
            targetAudience=None, 
            workload=None, 
            timeAvailable=None, 
            topics=None, 
            backgroundUrl='https://tc.com.br/wp-content/uploads/2021/07/comoescolher_thumb.png',
            sequential=1, 
            categoryId='5db1a95f0b19960058b9e188', 
            published=1,
            subscriptionsCount=0, 
            active=1, 
            dropoutPercentage=110.00, 
            isOpenCourse=1, 
            imgMobileUrl='https://tc.com.br/wp-content/uploads/2021/07/comoescolher_banner_mobile.png',
            imgBannerUrl='https://tc.com.br/wp-content/uploads/2021/07/comoescolher_banner_web.png'

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
                IsBonus=data['Bonus'].iloc[i]
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
    elif insert == 'refference':
        for i in range(data.shape[0]):
            if pd.isna(data['Links Referência'].iloc[i]) or data['Links Referência'].iloc[i] == '':
                continue
            if i==0 or data['Nome Aula'].iloc[i-1]!=data['Nome Aula'].iloc[i]:
                order = 1
            elif pd.isna(data['Links Referência'].iloc[i-1]) or data['Links Referência'].iloc[i-1] == '':
                order = 1
            else:
                order += 1

            result = writer.insert_refference(
                LectureName=data['Nome Aula'].iloc[i],
                ModuleName=data['Nome Módulo'].iloc[i], 
                CourseName=data['Curso'].loc[0], 
                ReffUrl=data['Links Referência'].iloc[i], 
                Order=order,
                Title='Nome Link Referência',
                Description=None
            )

    elif insert == 'file':                
        result = writer.file_get_infos(data)

    return result



insert='refference' #{'trail', 'course', 'module', 'lecture', 'product', 'coursetrail', 'article', 'refference','file'}
env = 'hml'

trail = 'Aprenda a investir'
CourseTrailOrder=4
productId = 64

name = 'Investimento Ideal.csv'

if 'experience' in name:
    for turma in [1,2]:
        data = pd.read_csv(f'~/Downloads/TCSchool - files/{name}') if insert not in {'trail'} else None
        productId += turma
        data['Curso'] += f' - Turma {turma}'
        result = main(insert, data=data, trail=trail, update=True, order=10, productId=productId, CourseTrailOrder=CourseTrailOrder, env=env)
else:
    data = pd.read_csv(f'~/Downloads/TCSchool - files/{name}') if insert not in {'trail'} else None
    result = main(insert, data=data, trail=trail, update=True, order=10, productId=productId, CourseTrailOrder=CourseTrailOrder, env=env)

