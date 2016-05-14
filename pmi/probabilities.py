"""probabilities.py: computes the PMI (Pointwise mutual information) with odds in order to boost the terms that occur in many positive news and in few negative news.
   We used a binary probabilistic model (BPM), i.e., we considers only if the news contains or not the term.
   p(x) was ignored when we applied odds
   p(y) was ignored because it is constante for all terms
   We used alfa=0.5 to avoid zero division error and to fix the scores between 0.5 and 1

"""
import math

__author__      = "Edimar Manica"


def p_p(pnx, pn):
    """
        Computes the probability of the term x occurs in POSITIVE news

        Args:
            pnx (int): number of POSITIVE news with the term x
            pn (int): number of POSITIVE news

        Returns:
            float: p(x|y)
        """
    return float(pnx)/pn

def p_n(nnx, nn):
    """
        Computes the probability of the term x occurs in NEGATIVE news

        Args:
            nnx (int): number of NEGATIVE news with the term x
            nn (int): number of NEGATIVE news

        Returns:
            float: p(x|not(Y))
        """
    return float(nnx) / nn

def _pmi_odds_(p_p, p_n):
    """
        Computes the PMI with odds

        Args:
            p_p (float): p(x|y)
            p_n (float): p(x|not(y)

        Returns:
            float: PMI
        """
    #print (p_p, p_n)
    alfa = 0.5
    return math.log(((p_p * (1-p_n))+alfa) / ((p_n* (1-p_p))+alfa))


def pmi_odds(pnx, pn, nnx, nn):
    """
        Computes the PMI with odds

        Args:
            pnx (int): number of POSITIVE news with the term x
            pn (int): number of POSITIVE news
            nnx (int): number of NEGATIVE news with the term x
            nn (int): number of NEGATIVE news

        Returns:
            float: PMI
        """
    #print (pnx, pn, nnx, nn)
    return _pmi_odds_(p_p(pnx, pn), p_n(nnx, nn))