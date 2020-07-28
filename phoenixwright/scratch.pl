% meta
:-style_check(-discontiguous).

% boilerplate rules
spouse(X,Y) :- married(X,Y).
husband(X,Y) :- male(X), married(X,Y).
wife(X,Y) :- female(X), married(X,Y).
father(X,Y) :- male(X), parent(X,Y).
mother(X,Y) :- female(X), parent(X,Y).
sister(X,Y) :- female(X), sibling(X,Y).
sibling(X,Y) :- father(Z,X), father(Z,Y), mother(W,X), mother(W,Y), not(X=Y).

dead(X,Y) :-

% phoenix
male(phoenix).
occupation(phoenix,attorney).

% redd white
male(redd).

% gumshoe
male(gumshoe).
occupation(gumshoe,detective).

% mia
female(mia).

% maya
female(maya).

% maya,mia father
male(fatherfey).
parent(fatherfey,maya).
parent(fatherfey,mia).

% maya,mia mother
female(misty).
parent(misty,maya).
parent(misty,mia).

% case
event(000,enter(maya,office)).
event(010,phone(maya,phoenix)).
event(020,enter(redd,office)).
event(030,take(redd,thinker)).
event(040,break(redd,lamp)).
event(041,transform(lamp,shards)).
event(050,kill(redd,maya)).
event(060,write(redd,receipt)).
event(070,enter(maya,office)).


