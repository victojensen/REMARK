# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     notebook_metadata_filter: all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.6.9
#   latex_envs:
#     LaTeX_envs_menu_present: true
#     autoclose: false
#     autocomplete: false
#     bibliofile: biblio.bib
#     cite_by: apalike
#     current_citInitial: 1
#     eqLabelWithNumbers: true
#     eqNumInitial: 1
#     hotkeys:
#       equation: Ctrl-E
#       itemize: Ctrl-I
#     labels_anchors: false
#     latex_user_defs: false
#     report_style_numbering: false
#     user_envs_cfg: false
# ---

# %% [markdown]
# # Optimal Portfolio Choice over the Life Cycle
#
# Economists like to compare actual behavior to the choices that would be made by a "rational" agent who understands all the complexities of a decision, and who knows how to find the mathematically optimal choice that takes those complexities into account.  
#
# Often, however, finding the optimal choice is remarkably difficult. Economists use computational tools that descend directly from the tools used originally by physicists and engineers to calculate, for example, the "optimal" trajectories for the Apollo spacecraft. 
#
# Surprisingly, calculating how much to save for retirement, and the optimal proportion of your portfolio to put in risky assets, is a **much** harder problem than performing the calculations for landing on the moon.  In fact, only in 2005 was the first academic paper published that made such calculations in a way realistic enough to take seriously (as we describe below).  
#
# Even today, these tools so difficult that it can take years of work for a new researcher to get to the point of being able to solve such problems themselves.  So much work is needed because each economist (or team of coauthors) has tended to construct from scratch their own elaborate and complex body of computer code tailored to solving exactly the problem they are interested in; rather than "standing on the shoulders of giants" in the great scientific tradition, everyone has had to grow to the stature of a giant themselves.
#
# The aim of the [Econ-ARK](https://econ-ark.org) toolkit is to address that problem by providing a set of open source software tools that can solve many computationally difficult models of optimal consumer choice; one of the early contributions of the toolkit was a tool that calculates optimal retirement saving under mostly realistic assumptions -- except that, to reduce complexity, the model makes the assumption that the consumer has no choice of how to invest their savings in "risky" (think stocks) versus "safe" (think bank accounts) assets.
#
# This blog post introduces a new tool in the toolkit, whose development was generously funded by the Think Forward Institute, that incorporates the optimal choice of portfolio share between "risky" assets which yield a higher expected (but not guaranteed) return, and "safe" assets.

# %% [markdown]
# ## The Problem
#
# Nobody saving for retirement knows exactly what the future holds. They might change jobs several times between now and retirement; they might have to retire early for health reasons, or they might be so robust that they want to work until age 75; even the future interest rates that will be earned on "safe" assets are not knowable in advance.
#
# This is why the consumer's problem is so much harder than the astronaut's: The motion of a spacecraft is almost perfectly predictable from Newton's equations.  If you set it in motion in a certain direction and with a certain velocity, you can calculate to within a matter of inches where it will be weeks in the future.
#
# The way economists calculate "optimal" behavior begins with an attempt to quantify each of the risks. For example, we have large datasets from which we can calculate how often people change jobs at each age of life, taking account of personal characteristics like education, occupation and so on, and on what happens to their income after job changes.  Job uncertainty can thus be represented mathematically as a statistical distribution over the many possible future outcomes, and similarly for other kinds of risk (like health risk). When all the individual risks have been quantified, we can calculate the joint probabilities of every conceivable draw of the risks, and weight each possible outcome by its probability.  Finally, we can calculate how the outcomes (like, for retirement income) depend on the choice of saving and portfolio choice.
#

# %% [markdown]
# ## The Solution
#
# ### Replicating the Standard Model
# Our first step has been to reproduce the results of the above-mentioned 2005 paper (by Cocco, Gomes, and Maenhout) using our new tool.  Although our results are different in some minor respects from theirs (likely having to do with different assumptions about the details of the risks), we are able to replicate their main "big-picture" findings.
#
# The most striking conclusion of their paper was that the model implied that the average optimal portfolio share in the population says that the "risky portfolio share" is 100 percent for essentially everyone younger than their early thirties.  Thereafter the optimal risky share declines with age until around the date of retirement (assumed to be 65), then exhibits a slight increase after retirement (although the 5th and 95th percentile bands show that there is considerable variation in the simulated population depending how risks for individual simulated consumers turn out, and other factors).
#
# The attractive thing about constructing a formal model of this kind is that it is possible to dig into it and figure out why it produces the results it does.
#
# In this case, there are three elements at play:
#
# 1. The model assumes a substantial "equity premium" of 4 percent a year
#    * The "equity premium" is the amount by which stock returns are expected to exceed returns on riskless assets
#    * For a 25 year old, this means that the expected return for a dollar invested in stocks is expected to grow over the 40 years to age 65 by about 5 times ($1.04^{40}$) as much as a dollar invested in safe assets
# 1. Young people are assumed to start with little or no assets
#    * The model assumes that their income comes mostly from working in the labor market
#    * If you have only a small amount of wealth, the absolute dollar size of the risk you are taking by investing in the risky asset is small, so you focus more on the higher returns than on the (small) risk
# 1. By the age of retirement, you plan to finance a lot of your spending from your savings
#    * The model builds in a Social Security system, but Social Security benefits are not large enough to satisfy the optimizing consumer's spending desires in retirement
#    * Investing everything in the stock market (like a young person) would put a large proportion of your spending at risk from the fluctuations in the market
#    * The "equity premium" is nevertheless large enough to make it worthwhile to keep about half of your assets in stocks
#
# ![RShare_Means](figures/figure_Parameters_base/RShare_Means.png)

# %% [markdown]
# ### Sensitivity of Resuts to Assumptions
#
# Solving a model of this kind requires us to make many assumptions about things that are in practice unknowable.  
#
# Two particularly important assumptions are the one about the expected size of the equity premium, and the intensity of consumers' risk aversion.
#
# The figures below explore how the answers change with plausible alternative values of these parameters.

# %% [markdown]
# #### If People Believe The Equity Premium Will Be Smaller
#
# While 4 percent is a reasonable estimate of the equity premium in the past, it is possible that people either are unaware that the premium has been so large, or do not believe it will be as large in the future as in the past.
#
# The figure below shows the consequences if people believe the equity premium will be only two percent.  
#
# The shape of the figure is much the same as before; in particular, the youngest people still hold 100 percent of their portfolios in risky assets.  But the proportion of their portfolios that middle-aged and older people hold in equities falls from about 50 to about 20 percent.
#
# ![RShare_Means](figures/figure_equity_0p02/RShare_Means.png)
#

# %% [markdown]
# #### If People Are Less Risk Averse
#
# One caveat about the baseline results in the CGM paper is that those authors assumed that people have much greater aversion to risk in financial investments than than they do with respect to other financial choice (for example, purchasing insurance).  In fact, most of the literature other than that on portfolio choice assumes a degree of risk aversion about 1/2 to 1/3 as large as CGM do.  
#
# The figure below shows the model's implications if relative risk aversion takes a value of 3, which is conventional elsewhere in economics.  In that case, most people should have most or all of their savings in the stock market at most ages.  (The fact that people do not invest as much in the stock market as models like this recommend is called the "equity premium puzzle"). 
#
# Mridul: Could you add an experiment where RRA is 3?

# %% [markdown]
# ### Comparison to Data and Professional Advice

# %% [markdown]
# The pattern above is strikingly different from the actual choices that typical savers make.  
#
# The figure below shows the patterns of the risky shares of assets in the U.S. population by age, as measured in triennial waves of the _Survey of Consumer Finances_.  
#
# As the figure shows, the pattern of actual behavior is almost the opposite of what the model implies: Young people have a low proportion of their assets in risky assets, and the proportion gradually peaks in middle age before declining in retirement.
#
# Another interesting comparison is to the advice of professional investment advisors.  Though that advice can be quite sophistcated and nuanced, it is also sometimes codified in simple rules of thumb.  One of the most common of these is the "100-age" rule, which says that the percentage of your portfolio in risky assets should be equal to 100 minus your age, so that a 25 year old would have 75 percent in stocks while a 60 year old would have 40 percent in stocks.
#
# For people before retirement, at least the shape of the profile that advisors recommend is somewhat like the shape that comes out of the model.  While the rule would say that the 25 year old should put 75 percent of their savings in the stock market and the model says 100 percent, they agree that the proportion should be high, and also agree that the proportion should decline during your working life.
#
# However, the rule and the model disagree about what should happen after retirement.  The rule recommends steadily reducing your exposure to risky assets as you get older, while the model says that your exposure should remain at about the same level it was at late in your working life.
#
# The advisors, who have daily contact with real human beings, probably have an insight that the model does not incorporate:  Risk aversion may increase as you get older.  
#
# Risk aversion is remarkably difficult to measure, and economists' efforts to determine whether it increases with age have been inconclusive, with some papers finding [evidence for an increase](https://voxeu.org/article/effect-age-willingness-take-risks) (at least during working life) and others finding [little increase](https://onlinelibrary.wiley.com/doi/abs/10.1016/j.rfe.2003.09.010). It is plausible, though, that investment advisors have insight that is hard to extract from statistical patterns but easy to perceive in interactions between live human beings.  (New research suggests that any increases in risk aversion among older people reflect [cognitive decline](https://www.nature.com/articles/ncomms13822) associated with reduced ability to process information).
#
# The figure below explores what would happen if the model's default value of risk aversion increased steadily (linearly) after age 55.  (To be specific, the coefficient rises from 6 to 10 over that age range).
#
# (Figure here)
#

# %% [markdown]
# ### Other Experiments
#
# The `PortfolioConsumerType` tool makes it easy to explore other alternatives.  For example, after the CGM paper was published, better estimates [became available](https://doi.org/10.1016/j.jmoneco.2010.04.003) about the degree and types of income uncertainty that consumers face at different ages.  The most important finding was that the degree of uncertainty in earnings is quite large for people in their 20s but falls sharply and flattens out at older ages.  
#
# It seems plausible that this greater uncertainty in labor earnings could account for the fact that in empirical data young people have a low share of their portfolio invested in risky assets; economic theory says that an increase in labor income risk should [reduce your willingness to expose yourself to financial risk](https://www.jstor.org/stable/2951719).
#
# But the figure below shows that even when we update the model to incorporate the improved estimates of labor income uncertainty, the model still says that young people should have 100 percent of their savings in the risky asset.
#
#

# %% [markdown]
# #### Code
#
# The computer code to reproduce all of the figures in this notebook, and a great many others, can be executed by installing the HARK toolkit and cloning the REMARK repo.  The small unix program `do_all_code.sh` at the root level of the [REMARKs/CGMPortfolio] directory produces everything.
#
# The full replication of the CGM paper is referenced in a link below.

# %% [markdown]
# #### References
#
# Cocco, J. F., Gomes, F. J., & Maenhout, P. J. (2005). Consumption and portfolio choice over the life cycle. The Review of Financial Studies, 18(2), 491-533.  [doi.org/10.1093/rfs/hhi017](https://doi.org/10.1093/rfs/hhi017)
#
# Velásquez-Giraldo, Mateo and Matthew Zahn.  Replication of the Cocco, Gomes, and Maenhout (2005).  [REMARK](https://github.com/econ-ark/REMARK/blob/master/REMARKs/CGMPortfolio/Code/Python/CGMPortfolio.ipynb)
