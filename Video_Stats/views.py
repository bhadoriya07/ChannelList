from genericpath import exists
from hashlib import new
from itertools import count
from pstats import Stats
from typing import Counter
from xml.etree.ElementTree import Comment
from charset_normalizer import detect
from django.shortcuts import render,HttpResponse
import csv
from django.conf import settings
import requests
from Video_Stats.models import stats
from langdetect import detect
#import pandas as pd


def Data(video_ids,video_link,brand,brand_cat,cm_name,cost):
    
    temp_list = []
    counter = 0

    search_url = 'https://www.googleapis.com/youtube/v3/videos'

    for video_id in video_ids:
        parameter = {  
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,statistics,contentDetails',
            'id' : video_id
        }

        data = requests.get(search_url,params=parameter)
        results = data.json()['items']
        
        if(len(results)==0):
            data = {
                'videoLink': video_link[counter],
                'brand': brand[counter],
                'brand_category':brand_cat[counter],
                'cmName': cm_name[counter],
                'cost': cost[counter],
                'cost_perviews': 'NA',
                'inf_name' : 'NA',
                'videoLive_date': 'NA',
                'language': 'NA',
                'video_duration': 'NA',
                'views': 'NA',
                'total_comments': 'NA',
                'video_title' : 'NA',
                'channel_link' : 'NA',
                'category': 'NA'
            }
            temp_list.append(data)
            counter = counter+1
            print(temp_list)

        else:
            title = (results[0]['snippet']['title']).split(" ")
            temp = []
            for t in title:
                try: 
                    lang = detect(t)
                    if lang=='en' and 'English' not in temp:
                        temp.append("English"),
                    elif lang=='hi' and 'Hindi' not in temp:
                        temp.append("Hindi")
                    elif lang=='te' and 'Telugu' not in temp:
                        temp.append("Telugu")
                    elif lang=='ta' and 'Tamil' not in temp:
                        temp.append("Tamil")
                    elif lang=='mal' and 'Malayalam' not in temp:
                        temp.append("Malayalam")
                    elif lang=='kn' and 'Kannada' not in temp:
                        temp.append("Kannada")
                    elif lang=='or' and 'Oriya' not in temp:
                        temp.append("Oriya")
                    elif lang=='bn' and 'Bengali' not in temp:
                        temp.append("Bengali")
                    elif lang=='pa' and 'Punjabi' not in temp:
                        temp.append("Punjabi")
                    elif lang=='gu' and 'Gujarati' not in temp:
                        temp.append("Gujarati")
                    elif lang=='mr' and 'Marathi' not in temp:
                        temp.append("Marathi")
                    elif lang=='ur' and 'Urdu' not in temp:
                        temp.append("Urdu")
                    elif 'NA' not in temp:
                        temp.append("NA")
                except:
                    continue
            language = ('/'.join(temp))
            try: 
                comments = results[0]['statistics']['commentCount']
            except KeyError:
                comments = '0'
            s = (results[0]['contentDetails']['duration']).replace("PT","").replace("M",":").replace("S","").replace("H",":")
            if(len(s.split(':')[1])==1):
                duration = s.split(':')[0]+':'+'0'+(s.split(':')[1])
            elif(len(s.split(':')[1])==0):
                duration = s.split(':')[0]+':'+'00'
            else:
                duration = s

            cat_id = (results[0]['snippet']['categoryId'])
            category_url = 'https://www.googleapis.com/youtube/v3/videoCategories'
            param = {
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'part' : 'snippet',
                'id' : cat_id
            }
            category_data = requests.get(category_url,params=param)
            category_name = category_data.json()['items']
            category = (category_name[0]['snippet']['title'])

            data = {
                'videoLink': video_link[counter],
                'brand': brand[counter],
                'brand_category':brand_cat[counter],
                'cmName': cm_name[counter],
                'cost': cost[counter],
                'cost_perviews': round(int(cost[counter])/int(results[0]['statistics']['viewCount']),3),
                'inf_name' : results[0]['snippet']['channelTitle'],
                'videoLive_date': (results[0]['snippet']['publishedAt']).rpartition('T')[0],
                'language': language,
                'video_duration': duration,
                'views': results[0]['statistics']['viewCount'],
                'total_comments': comments,
                'video_title' : results[0]['snippet']['title'],
                'channel_link' :  f'https://www.youtube.com/channel/{ results[0]["snippet"]["channelId"] }',
                'category': category
            }
            temp_list.append(data)
            counter = counter+1
       
    for list in temp_list:
        sta = stats(videoLink=list["videoLink"],brand=list["brand"],brand_category=list["brand_category"],cm_name=list["cmName"],cost=list["cost"],inf_name=list["inf_name"],live_date=list["videoLive_date"],channel_link=list["channel_link"],inf_category=list["category"],video_duration=list["video_duration"],views_count=list["views"],cost_perviews=list["cost_perviews"],comments=list["total_comments"],video_title=list["video_title"],language=list["language"])
        sta.save()
    


# def saveData(video_id,video_link,brand,brand_cat,cm_name,cost):
#     search_url = 'https://www.googleapis.com/youtube/v3/videos'

#     parameter = {
#         'key' : settings.YOUTUBE_DATA_API_KEY,
#         'part' : 'snippet,statistics,contentDetails',
#         'id' : ','.join(video_id)
#     }

#     data = requests.get(search_url,params=parameter)
#     results = data.json()['items']
#     comments = []
#     for result in results:
#         try: 
#             comments.append(result['statistics']['commentCount'])
#         except KeyError:
#             comments.append('0')

#     cat_id = []
#     language = []
#     duration = []
#     for result in results:
#         cat_id.append(result['snippet']['categoryId'])
#         title = (result['snippet']['title']).split(" ")
#         temp = []
#         for t in title:
#             try: 
#                 lang = detect(t)
#                 if lang=='en' and 'English' not in temp:
#                     temp.append("English"),
#                 elif lang=='hi' and 'Hindi' not in temp:
#                     temp.append("Hindi")
#                 elif lang=='te' and 'Telugu' not in temp:
#                     temp.append("Telugu")
#                 elif lang=='ta' and 'Tamil' not in temp:
#                     temp.append("Tamil")
#                 elif 'English' not in temp:
#                     temp.append("English")
#             except:
#                 continue
#         language.append('/'.join(temp))
#         s = (result['contentDetails']['duration']).replace("PT","").replace("M",":").replace("S","").replace("H",":")
#         if(len(s.split(':')[1])==1):
#             duration.append(s.split(':')[0]+':'+'0'+(s.split(':')[1]))
#         elif(len(s.split(':')[1])==0):
#             duration.append(s.split(':')[0]+':'+'00')
#         else:
#             duration.append(s)
#     print(language)
#     category = []
#     category_url = 'https://www.googleapis.com/youtube/v3/videoCategories'
#     for cat in cat_id:
#         param = {
#             'key' : settings.YOUTUBE_DATA_API_KEY,
#             'part' : 'snippet',
#             'id' : cat
#         }
#         category_data = requests.get(category_url,params=param)
#         category_name = category_data.json()['items']
#         category.append(category_name[0]['snippet']['title'])
#     temp_list = []
#     counter = 0
#     for result in results:
#         data = {
#             'videoLink': video_link[counter],
#             'brand': brand[counter],
#             'brand_category':brand_cat[counter],
#             'cmName': cm_name[counter],
#             'cost': cost[counter],
#             'cost_perviews': round(int(cost[counter])/int(result['statistics']['viewCount']),3),
#             'inf_name' : result['snippet']['channelTitle'],
#             'videoLive_date': (result['snippet']['publishedAt']).rpartition('T')[0],
#             #'language': result['snippet']['defaultLanguage'],
#             'video_duration': duration[counter],
#             'views': result['statistics']['viewCount'],
#             'total_comments': comments[counter],
#             'video_title' : result['snippet']['title'],
#             'channel_link' :  f'https://www.youtube.com/channel/{ result["snippet"]["channelId"] }',
#             'category': category[counter]
#         }
#         temp_list.append(data)
#         counter = counter+1

#     for list in temp_list:
#         sta = stats(videoLink=list["videoLink"],brand=list["brand"],brand_category=list["brand_category"],cm_name=list["cmName"],cost=list["cost"],inf_name=list["inf_name"],live_date=list["videoLive_date"],channel_link=list["channel_link"],inf_category=list["category"],video_duration=list["video_duration"],views_count=list["views"],cost_perviews=list["cost_perviews"],comments=list["total_comments"],video_title=list["video_title"])
#         sta.save()



def showPage(request):
    stats_data = stats.objects.all()
    stats_data.delete()
    if request.method == 'POST':
        rows = []
        video_link = []
        brand = []
        brand_cat = []
        cm_name = []
        cost = []
        file = request.FILES["file"].readlines()
        for f in file:
            rows.append((f.decode('utf-8')))
        rows = [x.replace("\r\n","") for x in rows]
        for r in rows[1:]:
            row=r.split(",")
            for i in range(0,len(row)):
                if(i==0):
                    if row[i].count("youtu.be/")>0 or row[i].count("youtube.com/watch")>0:
                        video_link.append(row[i])
                    else:
                        break
                elif i==1:
                    brand.append(row[i])
                elif i==2:
                    brand_cat.append(row[i])
                elif i==3:
                    cm_name.append(row[i])
                else:
                    cost.append(row[i])

        video_id = []           
        for link in video_link[0:len(rows)-1]:
             if '&' in link:
                video_id.append(link.rpartition('&')[0][-11:])
             else:
                video_id.append((link[-11:]))
        Data(video_id,video_link,brand,brand_cat,cm_name,cost)

        # while len(video_id):
        #     temp_id = video_id[:50]
        #     temp_link = video_link[:50]
        #     temp_brand = brand[:50]
        #     temp_brandCat = brand_cat[:50]
        #     temp_cmName = cm_name[:50]
        #     temp_cost = cost[:50]
        #     Data(temp_id,temp_link,temp_brand,temp_brandCat,temp_cmName,temp_cost)
        #     del(video_id[:50])
        #     del(video_link[:50])
        #     del(brand[:50])
        #     del(brand_cat[:50])
        #     del(cm_name[:50])
        #     del(cost[:50])

        
    return render(request,'stats.html')


def downloadFile(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename="statsData.csv"'

    writer = csv.writer(response)

    writer.writerow(['Video Link','Brand','Brand Category','CM Name','Cost','Influencer Name','Video Live Date','Channel Link','Inf Category','Video Duration','Views','Cost per views','Total Comments','Video Title','Language'])

    stats_data = stats.objects.all()

    for data in stats_data:
        writer.writerow([data.videoLink,data.brand,data.brand_category,data.cm_name,data.cost,data.inf_name,data.live_date,data.channel_link,data.inf_category,data.video_duration,data.views_count,data.cost_perviews,data.comments,data.video_title,data.language])

    stats_data.delete()

    return response
