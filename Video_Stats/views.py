from hashlib import new
from itertools import count
from pstats import Stats
from typing import Counter
from django.shortcuts import render,HttpResponse
import csv
from django.conf import settings
import requests
from Video_Stats.models import stats

temp_list = []
def showPage(request):
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
                    video_link.append(row[i])
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
             video_id.append((link[-11:]))

        search_url = 'https://www.googleapis.com/youtube/v3/videos'

        parameter = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,statistics,contentDetails',
            'id' : ','.join(video_id)
        }

        data = requests.get(search_url,params=parameter)
        results = data.json()['items']

        cat_id = []
        for result in results:
            cat_id.append(result['snippet']['categoryId'])
        category = []
        category_url = 'https://www.googleapis.com/youtube/v3/videoCategories'
        for cat in cat_id:
            param = {
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'part' : 'snippet',
                'id' : cat
            }
            category_data = requests.get(category_url,params=param)
            category_name = category_data.json()['items']
            category.append(category_name[0]['snippet']['title'])
        counter = 0
        for result in results:
            data = {
                'videoLink': video_link[counter],
                'brand': brand[counter],
                'brand_category':brand_cat[counter],
                'cmName': cm_name[counter],
                'cost': cost[counter],
                'cost_perviews': int(cost[counter])/int( result['statistics']['viewCount']),
                'inf_name' : result['snippet']['channelTitle'],
                'videoLive_date': result['snippet']['publishedAt'],
                #'language': result['snippet']['defaultLanguage'],
                'video_duration': (result['contentDetails']['duration']).replace("PT","").replace("M",":").replace("S","").replace("H",":"),
                'views': result['statistics']['viewCount'],
                'total_comments': result['statistics']['commentCount'],
                'video_title' : result['snippet']['title'],
                'channel_link' :  f'https://www.youtube.com/channel/{ result["snippet"]["channelId"] }',
                'category': category[counter]
            }
            temp_list.append(data)
            counter = counter+1
        
        for list in temp_list:
            sta = stats(videoLink=list["videoLink"],brand=list["brand"],brand_category=list["brand_category"],cm_name=list["cmName"],cost=list["cost"],inf_name=list["inf_name"],live_date=list["videoLive_date"],channel_link=list["channel_link"],inf_category=list["category"],video_duration=list["video_duration"],views_count=list["views"],cost_perviews=list["cost_perviews"],comments=list["total_comments"],video_title=list["video_title"])
            sta.save()
    return render(request,'stats.html')


def downloadFile(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename="statsData.csv"'

    writer = csv.writer(response)

    writer.writerow(['Video Link','Brand','Brand Category','CM Name','Cost','Influencer Name','Video Live Date','Channel Link','Inf Category','Video Duration','Views','Cost per views','Total Comments','Video Title'])

    stats_data = stats.objects.all()

    for data in stats_data:
        writer.writerow([data.videoLink,data.brand,data.brand_category,data.cm_name,data.cost,data.inf_name,data.live_date,data.channel_link,data.inf_category,data.video_duration,data.views_count,data.cost_perviews,data.comments,data.video_title])

    stats_data.delete()
    # for list in temp_list:
    #     writer.writerow([list["videoLink"],list["brand"],list["brand_category"],list["cmName"],list["cost"],list["inf_name"],list["videoLive_date"],list["channel_link"],list["category"],list["video_duration"],list["views"],list["cost_perviews"],list["total_comments"],list["video_title"]])

    temp_list.clear()
    return response