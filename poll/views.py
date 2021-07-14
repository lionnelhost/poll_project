# views.py
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CreatePollForm
from .models import Poll
from django.contrib import messages


def homes(request):
    polls = Poll.objects.all()

    context = {
        'polls': polls
    }
    return render(request, 'poll/home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid:
            # new_poll = form.save(commit=False)
            # new_poll.author = request.user
            # new_poll.save()
            form.save()
            messages.success(request, 'Poll created with success!')
            return redirect('home')
    else:
        form = CreatePollForm()

    context = {'form': form}
    return render(request, 'poll/create.html', context)


def update(request, poll_id):
    # poll = Poll.objects.get(pk=poll_id)
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        form = CreatePollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.info(request, 'Poll updated with success!')
            return redirect('home')
    else:
        form = CreatePollForm(instance=poll)

    context = {
        'poll': poll,
        'form': form
    }
    return render(request, 'poll/update.html', context)


def delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    print(poll)
    print(request.method)
    if request.method == 'GET':
        poll.delete()
        messages.info(request, 'Poll delete with success!')
        return redirect('home')

    polls = Poll.objects.all()
    context = {
        'polls': polls,
    }
    return render(request, 'poll/home.html', context)


def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    context = {
        'poll': poll
    }
    return render(request, 'poll/results.html', context)


def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')
        poll.save()
        messages.info(request, 'Vote added with success!')
        return redirect('home')

    context = {
        'poll': poll
    }
    return render(request, 'poll/vote.html', context)
