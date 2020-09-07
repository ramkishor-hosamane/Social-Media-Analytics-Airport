from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .Modules import visualizer
import os
import pandas as pd

scrapping_results_context = {'path':'',"scrolls":'',
                                'is_result':False,

                            'is_msg':False,
                'msg':'',
            "total_reviews":0,
            "gmap_res_length":0,
            "facebook_res_length":0,
            "trip_res_length":0,
            "twitter_res_length":0,
            "data":0,
            }

analysis_results_context = {
                'is_result' :False,
                                    
                'is_msg':False,
                'msg_type':'',
                'msg':'',
                'msg':'',
                'pos_reviews':'',
                "neg_reviews":'',
                'topic_wise':'',
                'word_cloud':'',
                'star_rating':'',
                'pie_pos_neg':'',
                'pie_topic':'',
                'bar_categarized_topic_pos_neg':'',

            }
def index(request):
    from .Modules import airport_links

    print([link for link in airport_links.links])

    return render(request,'home/Home.html')


def scrapping(request):
    global scrapping_results_context
    import threading
    from multiprocessing import Queue
    from .Modules import scarpers

    def scrape_reviews(path,scrolls,facebook_check,googlemap_check,tripadvisor_check,twitter_check,hashtag):

        result = {"Google Maps":0,"Facebook":0,"TripAdvisor":0,"Twitter":0}
        
        que = Queue()
        thread_list = []
        if googlemap_check:
            thread_list.append(threading.Thread(target=lambda q, arg1,arg2: q.put(scarpers.GmapScrap(arg1,arg2)),args=(que,path,scrolls,)))
        if facebook_check:
            thread_list.append(threading.Thread(target=lambda q, arg1,arg2: q.put(scarpers.facebookScrap(arg1,arg2)),args=(que,path,scrolls,)))
        if tripadvisor_check:
            thread_list.append(threading.Thread(target=lambda q, arg1,arg2: q.put(scarpers.tripAdvisorScrap(arg1,arg2)),args=(que,path,scrolls,)))
        if twitter_check:
            thread_list.append(threading.Thread(target=lambda q, arg1,arg2,arg3: q.put(scarpers.twitterScrap(arg1,arg2,arg3)),args=(que,path,scrolls,hashtag,)))        
        for t in thread_list:
            t.daemon = True
            t.start()
        for t in thread_list:
            t.join()
        
        while not que.empty():
            res = que.get()
            result[res[0]] = res[1]
        
        for pltfrm in result:
                if pltfrm=="Google Maps":
                    try:
                        result[pltfrm] = len(pd.read_csv(path+'/Scrapped Reviews/gmap_reviews.csv'))
                    except Exception as e:
                        print(e) 
                        result[pltfrm]=0
                elif pltfrm=="Facebook":
                    try:
                        result[pltfrm] = len(pd.read_csv(path+'/Scrapped Reviews/facebook_reviews.csv')
    )
                    except Exception as e:
                        print(e)
                        result[pltfrm]=0
                elif pltfrm=="TripAdvisor":
                    try:
                        result[pltfrm] = len(pd.read_csv(path+'/Scrapped Reviews/tripadvisor_reviews.csv'))
                    except Exception as e:
                        print(e)
                        result[pltfrm]=0
                elif pltfrm=="Twitter":
                    try:
                        result[pltfrm] = len(pd.read_csv(path+'/Scrapped Reviews/twitterdata.csv'))
                    except Exception as e:
                        print(e)
                        result[pltfrm]=0
                                                                    
                    
        
        return result


    def scrape_food_shop_reviews(path,scrolls):
        from .Modules import shop_links

        
        que = Queue()
        thread_list = []
        for shop in shop_links.links:
            thread_list.append(threading.Thread(target=lambda q, arg1,arg2,arg3,arg4: q.put(scarpers.GmapScrap(arg1,arg2,arg3,arg4)),args=(que,path,scrolls,'food.'+shop,shop_links.links[shop],)))        

        for t in range(2):
            thread_list[t].daemon = True
            thread_list[t].start()
        for t in range(2):
            thread_list[t].join()
        for t in range(2,4):
            thread_list[t].daemon = True
            thread_list[t].start()
        for t in range(2,4):
            thread_list[t].join()



    def scrape_other_reviews(other_airports,path,scrolls):
        result = {}
        que = Queue()
        thread_list = []
        for airport_name in other_airports:
            airport_link = airport_links.links.get(airport_name.strip().lower(),None)
            thread_list.append(threading.Thread(target=lambda q, arg1,arg2,arg3,arg4: q.put(scarpers.GmapScrap(arg1,arg2,arg3,arg4)),args=(que,path,scrolls,airport_name,airport_link,)))        
            
        for t in thread_list:
            t.daemon = True
            t.start()
        for t in thread_list:
            t.join()
                
        while not que.empty():
            res = que.get()
            result[res[2]] = res[1]        

        for airport_name in result:
            try:
                result[airport_name] = len(pd.read_csv(path+'/Scrapped Reviews/OtherAirports/'+airport_name+'.csv'))
                print(airport_name,'-->',result[airport_name])
            except Exception as e:
                print(e) 
                #result[airport_name]=0

        return result    









    if "clear_results" in request.POST:
        scrapping_results_context = {
                    'is_result':False,
                    'is_msg':True,
                    'msg_type':'Success',
                    'msg':'Results Cleared',
                    'path':'',"scrolls":'',
                    "total_reviews":0,
                    "gmap_res_length":0,
                    "facebook_res_length":0,
                    "trip_res_length":0,
                    "twitter_res_length":0,
                    "data":0,
                    }
        return render(request,'home/scrapping.html',scrapping_results_context)

    
    elif request.method == "POST":
        
        msg_type = "error"
        
        
        scrolls = request.POST.get('scrolls')
        path = request.POST.get('path')
        path = "home/"+path
        facebook_check  = request.POST.get("facebook")
        googlemap_check  = request.POST.get("googlemap")
        tripadvisor_check  = request.POST.get("tripadvisor")
        twitter_check  = request.POST.get("twitter")
        hashtag = request.POST.get("hashtag")
        other_airports = [request.POST[word] for word in request.POST if word[:7] == 'airport']
        print(other_airports)
        print()
        print(facebook_check,googlemap_check,tripadvisor_check,twitter_check)
        
        other_airport_res={}
            #scrolls=20
        print(scrolls,path,facebook_check)
        # create folder in the path
        try:
            os.mkdir(path)
            os.mkdir(path+"/Scrapped Reviews")
            os.mkdir(path+"/Output")
            os.mkdir(path+"/Reports")
            os.mkdir(path+"/Scrapped Reviews/OtherAirports")
           
        except Exception as e:
            print(e)
            print("Something went wrong")
            msg = "Name already exists"
            #scrapping_results_context = {'path':'',"scrolls":''}
            #return render(request,'home/scrapping.html',scrapping_results_context)
        all_blr_scraped_res = scrape_reviews(path,scrolls,facebook_check,googlemap_check,tripadvisor_check,twitter_check,hashtag)
        count_scrapped_reviews = visualizer.plot_count_scrapped_reviews(path,all_blr_scraped_res)
        
        if googlemap_check:
            scrape_food_shop_reviews(path,scrolls)
        
        if len(other_airports)>0:
            #other_airport_res = {"kokata":100,'dubai':200,'subai':300} 
            other_airport_res = scrape_other_reviews(other_airports,path,scrolls)
            print()
            
            print(other_airport_res)
        print(all_blr_scraped_res)
        scrapping_results_context = {'path':path,"scrolls":scrolls,'is_result':True,
                    'is_msg':True,
                    'msg_type':'Success',
                    'msg':'Scraping Completed',
                    "total_reviews":sum(list(all_blr_scraped_res.values())),
                    "gmap_res_length":all_blr_scraped_res["Google Maps"],
                    "facebook_res_length":all_blr_scraped_res["Facebook"],
                    "trip_res_length":all_blr_scraped_res['TripAdvisor'],
                    "twitter_res_length":all_blr_scraped_res['Twitter'],
                    "data":count_scrapped_reviews,
                    "other_airport_res":other_airport_res,
                    }
        return render(request,'home/scrapping.html',scrapping_results_context)  
    else:
        scrapping_results_context['is_msg'] = False
        return render(request,'home/scrapping.html',scrapping_results_context)

def analysis(request):
    global analysis_results_context
    from .Modules import analyser
    from .Modules import preprocesser
    import shutil
    def get_other_airport_comparison_plots(path,catogarized_final_res):
        other_airport_comparison_plots = {}
        blr_pos = [len(catogarized_final_res[topic]['pos']) for topic in catogarized_final_res]
        blr_neg = [len(catogarized_final_res[topic]['neg']) for topic in catogarized_final_res]

        for file in os.listdir(path+"/Scrapped Reviews/OtherAirports/"):
            other_airport_name = file.split('.')[0]
            other_df = pd.read_csv(path+"/Scrapped Reviews/OtherAirports/"+file)
            #other_df = other_df[other_df['Time']=="a year ago"]
            other_df = preprocesser.preprocess(other_df)
            other_final_res = analyser.get_catogarized_review(other_df)
            other_catogarized_final_res = analyser.get_catogarized_topic_sentiment_review(other_final_res)
            other_pos = [len(other_catogarized_final_res[topic]['pos']) for topic in other_catogarized_final_res]
            other_neg = [len(other_catogarized_final_res[topic]['neg']) for topic in other_catogarized_final_res]
            other_airport_comparison_plots[other_airport_name] = visualizer.plot_comparision(path,blr_pos,blr_neg,other_pos,other_neg,"Bangalore",other_airport_name)
        
        return other_airport_comparison_plots

    def get_food_shop_outlet_plot(path):
        res = ""
        try:
            sub_df = pd.read_csv(path+"/Scrapped Reviews/subway.csv")
            sub_df = preprocesser.preprocess(sub_df)
            sub_df["Sentiment"] = analyser.get_Sentiment(sub_df)

            ccd_df = pd.read_csv(path+"/Scrapped Reviews/cafe coffee day.csv")
            ccd_df = preprocesser.preprocess(ccd_df)
            ccd_df["Sentiment"] = analyser.get_Sentiment(ccd_df)

            tif_df = pd.read_csv(path+"/Scrapped Reviews/tiffin center.csv")
            tif_df = preprocesser.preprocess(tif_df)
            tif_df["Sentiment"] = analyser.get_Sentiment(tif_df)

            urb_df = pd.read_csv(path+"/Scrapped Reviews/urban.csv")
            urb_df = preprocesser.preprocess(urb_df)
            urb_df["Sentiment"] = analyser.get_Sentiment(urb_df)
            res = visualizer.plot_shops(path,sub_df,ccd_df,tif_df,urb_df)


        except Exception as e:
            print("Exception ",e)
            pass
        return res
    def get_topic_res(final_res):
        topic_wise = {topic:[] for topic in final_res}
        url_wise = {topic:[] for topic in final_res}
        for topic in final_res:
            for rev in final_res[topic]:
                topic_wise[topic].append(rev[2])
                url_wise[topic].append(rev[1])

        return topic_wise,url_wise



    #if request.is_ajax():
        #print("jesson",request.POST)
        #return JsonResponse({'msg':'success'})
    
    #print("Hurray",request.is_ajax())  
    #print(request.POST)
    if "clear_results" in request.POST:
        analysis_results_context = {
                                    
                                    'is_msg':True,
                                    'msg_type':'Success',
                                    'msg':'Results Cleared',
                                    'path':'',
                                    'is_result' :False,
                                    'pos_reviews':'',
                                    "neg_reviews":'',
                                    'topic_wise':'',
                                    'word_cloud':'',
                                    'star_rating':'',
                                    'pie_pos_neg':'',
                                    'pie_topic':'',
                                    'bar_categarized_topic_pos_neg':'',

                                    }
        
        unwanted = set(['static', 'Modules', 'migrations', 'templates', 'Not_needed', '__pycache__', 'urls.py', 'samp.py', 'models.py', 'admin.py','tests.py','Spell.csv','__init__.py', 'views.py', 'apps.py'])
        valid_paths = set(os.listdir(os.getcwd()+"/home/"))
        valid_paths = valid_paths.difference(unwanted)
        
        analysis_results_context["valid_paths"] = valid_paths    

        #s = visualizer.plot_comparision('',[140,170,250,300],[267,130,353,235],[235,500,334,356],[324,134,334,234])
        return render(request,'home/analysis.html',analysis_results_context)

    elif request.method == "POST":

        path = request.POST.get('path')
        path = 'home/'+ str(path)
        print(path)
        revs = ["gmap_reviews.csv"]

        
        df = pd.read_csv(path+'/Scrapped Reviews/gmap_reviews.csv')
        df = preprocesser.preprocess(df)
        word_cloud = visualizer.word_cloud(df,path)
        star_rating = visualizer.star_rating(df,path)
        df['sentiment'] = analyser.get_Sentiment(df)
        pos_reviews = df[df['sentiment']=='pos']['Review'].values
        neg_reviews = df[df['sentiment']=='neg']['Review'].values
        pos_reviews_url = df[df['sentiment']=='pos']['Reviewer Profile URL'].values
        neg_reviews_url = df[df['sentiment']=='neg']['Reviewer Profile URL'].values

        final_res = analyser.get_catogarized_review(df)
        topic_wise,url_wise = get_topic_res(final_res)
        catogarized_final_res = analyser.get_catogarized_topic_sentiment_review(final_res)
        bar_categarized_topic_pos_neg = visualizer.bar_categarized_topic_pos_neg(catogarized_final_res,path)
        pie_pos_neg = visualizer.pie_pos_neg(df,path)
        pie_topic = visualizer.pie_topic(final_res,path)



        res_pos_df = {"Reviewer URL":pos_reviews_url,"Review":pos_reviews}
        res_neg_df = {"Reviewer URL":neg_reviews_url,"Review":neg_reviews}
        res_pos_df = pd.DataFrame(res_pos_df)
        res_neg_df = pd.DataFrame(res_neg_df)
        writer = pd.ExcelWriter(path+"/Reports/pos_neg_reviews.xlsx", engine='xlsxwriter')
        res_pos_df.to_excel(writer,sheet_name='positive_reviews', index = False)
        res_neg_df.to_excel(writer,sheet_name='negative_reviews', index = False)  
        writer.save()          





        res_food_df = {"Reviewer URL":url_wise['Food/Shopping'],"Review":topic_wise['Food/Shopping']}
        res_maintainance_df = {"Reviewer URL":url_wise['Maintenance/Clean'],"Review":topic_wise['Maintenance/Clean']}
        res_infrastructures_df = {"Reviewer URL":url_wise['Infrastructures'],"Review":topic_wise['Infrastructures']}
        res_security_df = {"Reviewer URL":url_wise['Security/Staff'],"Review":topic_wise['Security/Staff']}
        res_food_df = pd.DataFrame(res_food_df)
        res_maintainance_df = pd.DataFrame(res_maintainance_df)
        res_infrastructures_df = pd.DataFrame(res_infrastructures_df)
        res_security_df = pd.DataFrame(res_security_df)
        writer = pd.ExcelWriter(path+"/Reports/topic_reviews.xlsx", engine='xlsxwriter')
        res_food_df.to_excel(writer,sheet_name='Food_Shopping', index = False)
        res_maintainance_df.to_excel(writer,sheet_name='Maintenance_Clean', index = False)  
        res_infrastructures_df.to_excel(writer,sheet_name='Infrastructures', index = False)
        res_security_df.to_excel(writer,sheet_name='Security_Staff', index = False)
        writer.save()
        
        shutil.copy(path+"/Reports/topic_reviews.xlsx","home/static/home/Outputs/topic_reviews.xlsx")          
        shutil.copy(path+"/Reports/pos_neg_reviews.xlsx","home/static/home/Outputs/pos_neg_reviews.xlsx")          



        ''' Analysis of other airport results '''
        #s = visualizer.plot_comparision('',[140,170,250,300],[267,130,353,235],[235,500,334,356],[324,134,334,234])
        other_airport_comparison_plots = get_other_airport_comparison_plots(path,catogarized_final_res)
        
        food_shop_outlets = get_food_shop_outlet_plot(path)
        unwanted = set(['static', 'Modules', 'migrations', 'templates', 'Not_needed', '__pycache__', 'urls.py', 'samp.py', 'models.py', 'admin.py','tests.py','Spell.csv','__init__.py', 'views.py', 'apps.py'])
        valid_paths = set(os.listdir(os.getcwd()+"/home/"))
        valid_paths = valid_paths.difference(unwanted)

        analysis_results_context = {
                                                
                                    'is_msg':True,
                                    'msg_type':'Success',
                                    'msg':'Analysis Completed',
                                    'is_result' :True,
                                    'path':path.split('/')[1],
                                    'pos_reviews':pos_reviews,
                                    "neg_reviews":neg_reviews,
                                    'topic_wise':topic_wise,
                                    'pos_reviews_url':pos_reviews_url,
                                    'neg_reviews_url':neg_reviews_url,
                                    'url_wise':url_wise,
                                    'word_cloud':word_cloud,
                                    'star_rating':star_rating,
                                    'pie_pos_neg':pie_pos_neg,
                                    'pie_topic':pie_topic,
                                    'bar_categarized_topic_pos_neg':bar_categarized_topic_pos_neg,
                                    'other_airport_comparison_plots':other_airport_comparison_plots,
                                    'food_shop_outlets':food_shop_outlets,
                                    }



        analysis_results_context["valid_paths"] = valid_paths    
        
        shutil.make_archive("home/static/home/Outputs/"+path.split('/')[1], 'zip', path)

        return render(request,'home/analysis.html',analysis_results_context)
    
    else:
        #list valid paths
        unwanted = set(['static', 'Modules', 'migrations', 'templates', 'Not_needed', '__pycache__', 'urls.py', 'samp.py', 'models.py', 'admin.py','tests.py','Spell.csv','__init__.py', 'views.py', 'apps.py'])
        valid_paths = set(os.listdir(os.getcwd()+"/home/"))
        valid_paths = valid_paths.difference(unwanted)

        analysis_results_context['is_msg'] = False
        analysis_results_context["valid_paths"] = valid_paths    
        
        return render(request,'home/analysis.html',analysis_results_context)





def about(request):
    return render(request,"home/about.html")