from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Question, Vote

# Create your views here.

def signup(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')

		if password == confirm_password:
			if not User.objects.filter(username=username):
				user = User.objects.create_user(username=username, password=password)
				login(request, authenticate(username=username, password=password))
				return redirect('all_polls')
			else:
				return HttpResponse('Username already exists!')
		else:
			return HttpResponse('Password did not match!')

	return render(request, 'front/signup.html')

def enter(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			login(request, user)
			return redirect('all_polls')
		else:
			return HttpResponse('Incorrect username or password!')

	return render(request, 'front/login.html')

def exit(request):
	logout(request)

	return redirect('enter')

def reset_password(request):
	if not request.user.is_authenticated:
		return redirect('enter')

	username = request.user.username

	if request.method == 'POST':
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')

		if authenticate(username=username, password=old_password):
			user = User.objects.get(username=username)
			user.set_password(new_password)
			user.save()
			return redirect('all_polls')

		else:
			return HttpResponse('Incorrect old password!')

	return render(request, 'front/reset_password.html')

def all_polls(request):
	if not request.user.is_authenticated:
		return redirect('enter')

	username = request.user.username
	questions = Question.objects.all().order_by('-pk')
	polls = [[[questions[0].question, questions[0].username],[]]]
	count = 0
	
	for question in questions:
		if polls[count][0][0] == question.question:
			polls[count][1].append([question.option, question.count])
		else:
			count += 1
			polls.append([[question.question, question.username],[]])
			polls[count][1].append([question.option, question.count])

	for poll in polls:
		sum = 0
		for count in poll[1]:
			sum = sum + count[1]

		if sum >= 12:
			poll[0].append('complete')
		else:
			poll[0].append('remain')

		if Vote.objects.filter(voter=username, question=poll[0][0]):
			poll[0].append('voted')
		else:
			poll[0].append('not')

		for count in poll[1]:
			try:
				count.append((100*count[1])/sum)
			except:
				count.append(0)

	paginator = Paginator(polls, 5)
	page_number = request.GET.get('page')
	polls = paginator.get_page(page_number)
				
	return render(request, 'front/all_polls.html', {'username':username, 'polls':polls})

def my_polls(request):
	if not request.user.is_authenticated:
		return redirect('enter')

	username = request.user.username
	questions = Question.objects.filter(username=username)
	if questions:
		polls = [[[questions[0].question, questions[0].username],[]]]
		count = 0
		
		for question in questions:
			if polls[count][0][0] == question.question:
				polls[count][1].append([question.option, question.count])
			else:
				count += 1
				polls.append([[question.question, question.username],[]])
				polls[count][1].append([question.option, question.count])

		for poll in polls:
			sum = 0
			for count in poll[1]:
				sum = sum + count[1]

			if sum >= 12:
				poll[0].append('complete')
			else:
				poll[0].append('remain')

			if Vote.objects.filter(voter=username, question=poll[0][0]):
				poll[0].append('voted')
			else:
				poll[0].append('not')

			for count in poll[1]:
				try:
					count.append((100*count[1])/sum)
				except:
					count.append(0)
	else:
		polls=[]

	paginator = Paginator(polls, 5)
	page_number = request.GET.get('page')
	polls = paginator.get_page(page_number)

	return render(request, 'front/my_polls.html', {'username':username, 'polls':polls})

def create_poll(request):
	if not request.user.is_authenticated:
		return redirect('enter')

	username = request.user.username

	if request.method == 'POST':
		username = request.user.username
		question = request.POST.get('question')
		options = []
		options.append(request.POST.get('option1'))
		options.append(request.POST.get('option2'))
		options.append(request.POST.get('option3'))
		options.append(request.POST.get('option4'))
		options.append(request.POST.get('option5'))
		
		while True:
			try:
				options.remove('')
			except:
				break

		if question == '':
			return HttpResponse('Enter a question!')
		elif len(options)<2:
			return HttpResponse('Enter at least 2 options!')

		for option in options:
			polls = Question(username=username , question=question, option=option, count=0)
			polls.save()

		return redirect('my_polls')
	return render(request, 'front/create_poll.html', {'username':username})

def delete_poll(request, username, question):
	question = Question.objects.filter(username=username, question=question)
	vote = Vote.objects.filter(username=username, question=question)
	question.delete()
	try:
		vote.delete()
	except:
		pass

	return redirect('my_polls')

def vote(request, username, question, option):
	vote = Vote(voter=request.user.username, username=username, question=question, option=option)
	vote.save()
	question = Question.objects.get(username=username, question=question, option=option)
	question.count += 1
	question.save()

	return redirect('all_polls')