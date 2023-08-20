# What is the purpose of this project?
In this project, we will develop the concept of epigenetic learning in a simple video game model.

# What is epigenetics?
In nature, epigenetics is the process by which specific genes are activated or deactivated in response to environmental conditions. For example, animals which are starving have genes 
which reduce metabolism turn on. 

Epigenetic information can be inherited, though more weakly than full genes.

# Lamarckian Inheritance
A related concept is the outdated theory of Lamarckian inheritance, which claimed that behavioral traits led to physical changes in offspring - for example, Lamarck postulated that giraffes gained their long necks due to their parents reaching further for leaves. Although this does not accurately describe real life evolution, it could be useful for the purpose of developing more vibrant and versatile AI.

# What is epigenetic learning in the context of video games?
In the context of video games, epigenetics most closely maps to adjusting behavioral weights on the fly - in our model, choosing which mode of attack to use to deal the most damage given the context of the resources available and the enemies being fought. For example, the agent might learn to use fire damage against frost enemies.

# What is the difference between epigenetic learning and more standard genetic learning in the context of video games?
Standard genetic learning simulates the transmission of genes using crossover and mutation when an agent’s “run” terminates, weighting this crossover based on metrics which calculate the agent’s fitness over the course of its life. 

Epigenetic learning would instead tweak behaviors in real time based on feedback from the environment - in our case, the agent might see its normal attacks do little damage against frost enemies, and experiment with other damage types until it finds one which works better.

In our context, we should have genes code for larger-scale behaviors (perhaps new damage types themselves?) whereas epigenes would code for weights on these behaviors.
