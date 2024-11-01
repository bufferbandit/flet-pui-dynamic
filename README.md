During my research into Flet, I came across the (PUI Framework)[https://github.com/buganini/PUI]. 
I instanly loved the ability to write reactive Flet code (à la Svelte) and the fact that it makes Flet declarative (way less ugly paradigm imo) made it even better.

However, PUI is not a Flet framework per se and is framework agnostic and 
only a couple of Flet controls had been implemented, manually.


My goal was to create a solution that can use PUI with any Flet module.
Additionally, the code will allow the use of declarative context managers 
on other attributes, including those that support a single child, like the content attribute on the Container.
