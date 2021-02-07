from django.shortcuts import render, redirect
from django.urls import reverse
from bs4 import BeautifulSoup
import urllib.request
import operator
import itertools 
# Create your views here.

def home(request):
    if request.method == 'POST':
        url = request.POST.get('raw_url', '')
        webUrl  = urllib.request.urlopen(url)
        word_list = []

        raw_html = webUrl.read()
        soup = BeautifulSoup(raw_html)
        for text in soup.find_all(text=True):
            content = text.string
            words = content.lower().split()
            for w in words:
                word_list.append(w)
        clean_words = []
        common_words =['the', 'if', 'go', 'vs', 'at', 'there', 'some', 'my', 'of', 'be', 'use','and', 'this','an','a',	'to', 'in', 'or', 'is', 'you', 'by', 'it']
        for word in word_list:
            symbols = "!-=@#$%^&*()<>?:\"{}|,./;\'[]`~1234567890"
            for i in range(0, len(symbols)):
                word = word.replace(symbols[i], "")
            if (len(word) > 0) and (len(word) < 20) and word not in common_words:
                clean_words.append(word)
        count = {}
        for word in clean_words:
            if word in count:
                count[word] += 1
            else:
                count[word] = 1
        for key, value in sorted(count.items(), key=operator.itemgetter(1)):
            count[key] = value
        global res
        res = dict(itertools.islice(count.items(), 10))
        return redirect('/result/')
    return render(request, 'home.html')

def result(request):
    context = dict(res)
    new_d = dict(sorted(context.items(), key=lambda item: item[1],reverse=True))
    list = [(k, v) for k, v in new_d.items()]
    print(list)
    return render(request, 'result.html', {'list':list})