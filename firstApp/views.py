from multiprocessing import context
from urllib import response
from django.shortcuts import render,HttpResponse
from django.conf import settings
import requests
import csv
from django.http import StreamingHttpResponse

channel_list = []

def home(request):
    context = {'message' : ""}
    if request.method == 'POST':
        print("channel list at first: ")
        print(channel_list)
        rows = []
        video_id = []
        file = request.FILES["file"].readlines()

        for f in file:
            rows.append((f.decode('utf-8')))
        

        for row in rows[0:len(rows)-1]:
             video_id.append((row[-13:]))
        video_id.append((rows[len(rows)-1][-11:]))

        video_id = [x.replace("\r\n","") for x in video_id]

        print("Video id:")
        for video in video_id:
            print(video)

        search_url = 'https://www.googleapis.com/youtube/v3/videos'

        parameter = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet',
            'id' : ','.join(video_id)
        }

        data = requests.get(search_url,params=parameter)
        results = data.json()['items']

        temp_list = []

        for result in results:
            data = {
                'name' : result['snippet']['channelTitle'],
                'url' :  f'https://www.youtube.com/channel/{ result["snippet"]["channelId"] }'
            }
            temp_list.append(data)
        
        [channel_list.append(x) for x in temp_list if x not in channel_list]
        
        print("channel list at home:")
        print(channel_list)
        
        context['message'] = "Click on Download File to download the file"

    return render(request,'index.html',context)

def exportfile(request):


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename="channelUrls.csv"'

    writer = csv.writer(response)

    print("channel list at exportfile:")
    print(channel_list)
    
    for list in channel_list:
        writer.writerow([list['url']])
    channel_list.clear()
    return response