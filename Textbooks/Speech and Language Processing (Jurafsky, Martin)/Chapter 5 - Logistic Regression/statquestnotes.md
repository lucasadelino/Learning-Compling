A review of the fundamental concepts in statistics that are used in this chapter, as taught by the StatQuest channel on YouTube.

# Probability ≠ Likelihood

Probability is the area of the curve under a probability distribution **GIVEN** the probability distribution

Likelihood is a probability distribution **GIVEN** a specific value or series of values

Thus when we talk about maximum likelihood estimation, we are talking about fitting a probability distribution to a series of values. In other words, we’re answering the question: which probability distribution makes these values most likely?

## Odds ≠ Probability

Odds are the chances of something happening versus it not happening

Probabilities are the chances of something happening versus **all possible outcomes** (happening **and** not happening).

You can convert a probability to odds like this: $odds = \frac{p}{(1-p)}$

# Review

## Linear Regression

[https://www.youtube.com/watch?v=PaFPbb66DxQ&t=0s](https://www.youtube.com/watch?v=PaFPbb66DxQ&t=0s)

The goal of linear regression is to fit a line through several points of data. You do that through the sum of squared residuals (a residual is the distance between a point and a line). The sum of the squared residuals is a type of *loss function*.

## Logistic Regression

[https://www.youtube.com/watch?v=yIYKR4sgzI8](https://www.youtube.com/watch?v=yIYKR4sgzI8)

Like Linear Regression, Logistic Regression aims to fit a distribution to data, but it’s a sigmoid instead of a line. Logistic regression is what you use when you have binary data (yes/no, true/false, heads/tails, etc). It’s also what you use if you want to take probabilities: you pass your values to the logistic function which maps them in a sigmoid:

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d7059aca-3505-4637-97f1-76967ecf1b7b/Untitled.png)

## Gradient Descent

[https://www.youtube.com/watch?v=sDv4f4s2SB8&t=0s](https://www.youtube.com/watch?v=sDv4f4s2SB8&t=0s)

Schedule

## Stochastic Gradient Descent

[https://www.youtube.com/watch?v=vMh0zPT0tLI&t=182s](https://www.youtube.com/watch?v=vMh0zPT0tLI&t=182s)

Stochastic Gradient Descent is a way of doing Gradient Descent that is well-suited for big data. Here’s the difference: with each step, instead of taking the gradient with respect to all samples, it chooses a single sample. This dramatically reduces the calculations made for each step. A slightly more complex (but still very efficient) way of doing this is called **mini-batch training**, where instead of using only one sample, you use a few samples (like three or four or five) in each step.