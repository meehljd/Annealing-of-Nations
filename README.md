# Annealing-of-Nations
Use Simulated Annealing to solve Taveling Salesperson Problem.  The goal is to find a near-optimum multi-city flight route to complete a tour of the countries listed in the They Might Be Giants song "Alphabet of Nations".

**Motivation:** Integrate various coding and algorithm skills into a full-stack solution. 

nations = [Algeria, Bulgaria, Cambodia, Dominica, Egypt, France, Gambia, Hungary, Iran, Japan, Kazakhstan, Libya Mongolia, Norway, Oman, Pakistan, Qatar, Russia, Suriname, Turkey, Uruguay, Vietnam, West Xylophone*, Yemen, Zimbabwe]
*Use Greece, due to etymology of the word xylophone.

**Video:** https://www.youtube.com/watch?v=drgrvDypOjA

## Solution Stack

**Flight Data:** Use solution from "Flight Deal Finder" capstone project (Day 39 - 100 Days of Code Challenge)
- Flight Data API: https://tequila.kiwi.com/portal/login
- Choose flights from most populous city in each country.
- Validate flight exists for low-population countries.  May need to substitute other countries...
- Course Videos: https://www.udemy.com/course/100-days-of-code/learn/lecture/21371844#overview
- Code: https://github.com/meehljd/100DaysOfCode/tree/master/Day39_Flight_Deals

**Optimization:** Use annealing simulation.
- 
**Front-End:** Map of route using Flask and Jinja...
- Inputs:  Optimize for distance/cost, rerun.
- Outputs:  Visual of flight path on map, total cost and distance of optimum rounte.  May include distance & cost of least optimum route as well.

## TODO

Everything...
