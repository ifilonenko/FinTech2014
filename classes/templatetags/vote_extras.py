from django import template
from polls.models import Vote

register = template.Library()

@register.filter(name='get_votes')
def get_votes(cork_basket, choice):
    # cork_basket = CorkBasketMembership.objects.filter(cork=cork, basket=basket)
    return Vote.objects.filter(cork_basket=cork_basket, choice=choice)

@register.filter(name='filter_voting_round')
def filter_voting_round(votes, second_vote):
    # cork_basket = CorkBasketMembership.objects.filter(cork=cork, basket=basket)
    count = votes.filter(second_vote=second_vote).count()
    return count

