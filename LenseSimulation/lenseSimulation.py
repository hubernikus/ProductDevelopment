"""
Lense simulation using python

Author: Huber Lukas
Date> 2017/11/02

"""
## Import libraries
import numpy as np #math library
import matplotlib.pyplot as plt # figure plotting
from math import cos,sin,asin,acos, atan2, sqrt, pi


refractionIndex_air = 1.000277

class Lense():
    # Geometrical properties
    widthMin = 0.1 # [mm]
    rad_lens  = 30  # [mm]

    # Fraction Coefficient
    refractionIndex = 1.47 # Glycerol
    
    # Visulazation
    N_points = 10 # number of datapoints to plot each side

    def __init__(self, corr, posx):
        # Correction coefficient
        # Position in [mm], where the eye is at zero
        
        self.corr = corr
        
        self.posx = posx # possible? convert to [m]

        self.convex = np.sign(corr) #
        
        if self.convex>0:
            self.rad_curve = corr
            self.phi_lense = asin(self.rad_lens/self.rad_curve)

            self.pos0 = [self.posx-self.rad_curve*cos(self.phi_lense),
                     self.posx+self.rad_curve*cos(self.phi_lense)]

            plt.plot([self.pos0[0]+self.rad_curve*cos(-self.phi_lense+self.phi_lense*2/self.N_points*i)
                  for i in range(self.N_points+1)],
                 [self.rad_curve*sin(-self.phi_lense + self.phi_lense*2/self.N_points*i)
                  for i in range(self.N_points+1)],'k')

            plt.plot([self.pos0[1]-self.rad_curve*cos(-self.phi_lense+self.phi_lense*2/self.N_points*i)
                   for i in range(self.N_points+1)],
                  [self.rad_curve*sin(-self.phi_lense + self.phi_lense*2/self.N_points*i)
                   for i in range(self. N_points+1)],'k')
            
        elif self.convex < 0:
            self.rad_curve = -corr
            self.phi_lense = asin(self.rad_lens/self.rad_curve)
            
            self.pos0 = [self.posx-(self.widthMin/2+self.rad_curve),
                         self.posx+(self.widthMin/2+self.rad_curve)]

            dPhi = self.phi_lense*2/self.N_points # angle iteration for plot
            
            plt.plot([self.pos0[0]+self.rad_curve*cos(-self.phi_lense+dPhi*i)
                  for i in range(self.N_points+1)],
                 [self.rad_curve*sin(-self.phi_lense + dPhi*i)
                  for i in range(self.N_points+1)],'k')

            plt.plot([self.pos0[1]-self.rad_curve*cos(-self.phi_lense+dPhi*i)
                   for i in range(self.N_points+1)],
                  [self.rad_curve*sin(-self.phi_lense + dPhi*i)
                   for i in range(self. N_points+1)],'k')
            
            plt.plot([self.pos0[1]-self.rad_curve*cos(-self.phi_lense),
                      self.pos0[0]+self.rad_curve*cos(-self.phi_lense)],
                     [self.rad_curve*sin(-self.phi_lense),
                      self.rad_curve*sin(-self.phi_lense)],
                     'k')

            plt.plot([self.pos0[1]-self.rad_curve*cos(self.phi_lense),
                      self.pos0[0]+self.rad_curve*cos(self.phi_lense)],
                     [self.rad_curve*sin(self.phi_lense),
                      self.rad_curve*sin(self.phi_lense)],
                     'k')

        else:
            print('flat plate detected')

    def photonSimulation(self, photon):
        if self.convex:
            # Extract line parameters
            a = photon.dir
            b = photon.x0[1]-a*photon.x0[0]

            # Extract lense parameters
            x0 = self.pos0[1]
            r = self.rad_curve

            # Find point of intersection
            a1 = 1+a**2
            b1 = -2*a*b - 2*a**2*x0
            c1 = a**2*x0**2 + 2*a*b*x0 + b**2 - r**2

            dx = (-b1 + sqrt(b1**2-4*a1*c1))/(2*a1)

            x_in = x0-dx
            y_in = a*x_in+b

            plt.plot([photon.x0[0],x_in],[photon.x0[1],y_in])

            # Refraction of the light beam
            phi_in = atan2(y_in,dx)
            theta1_abs_in = atan2(a,1)
            theta1_rel_in = theta1_abs_in + phi_in
            theta2_rel_in = asin(refractionIndex_air/self.refractionIndex*sin(theta1_rel_in))
            theta2_abs_in = theta2_rel_in-phi_in

            plt.plot([self.pos0[1]-0.9*r*cos(phi_in), self.pos0[1]-1.1*r*cos(phi_in)],
                     [0.9*r*sin(phi_in), 1.1*r*sin(phi_in)],'k--')

            # Extract line parameters
            a = theta2_abs_in
            b = y_in-x_in

            # Extract lense parameters
            x0 = self.pos0[0]
            r = self.rad_curve

            # Find point of intersection
            a1 = 1+a**2
            b1 = 2*a*b + 2*a**2*x0
            c1 = a**2*x0**2 + 2*a*b*x0 + b**2 - r**2

            dx = (-b1 + sqrt(b1**2-4*a1*c1))/(2*a1)

            x_out = x0+dx
            y_out = a*x_in+b

            plt.plot([x_in,x_out],[y_in,y_out])

            phi_out = atan2(y_out,dx)
            theta1_abs_out = atan2(a,1)
            theta1_rel_out = theta1_abs_out - phi_out
            theta2_rel_out = asin(self.refractionIndex/refractionIndex_air*sin(theta1_rel_out))
            theta2_abs_out = theta2_rel_out + phi_out

            dr = 10
            plt.plot([self.pos0[0]+(r-dr)*cos(phi_out), self.pos0[0]+(r+dr)*cos(phi_out)],
                     [(r-dr)*sin(phi_out), (r+dr)*sin(phi_out)],'k--')

            print(self.pos0[1])
            return Line([x_out, y_out], theta2_abs_out)

            # n1 * sin theta = n2 * sin theta
#            N = 20
#            plt.plot(x0,0,'o')
#            plt.plot([x0+r*cos(i*2*pi/N) for i in range(N+1)],
#                     [r*sin(i*2*pi/N) for i in range(N+1)])


            
                        

class Line:
    def __init__(self, x0, dir):
        self.dir = dir;
        self.x0 = x0;

def lightSimulation(photon, lenses):
    for i in range(len(lenses)): # 
        photon = lenses[i].findInterection(photon)

    # Intersection with horizontal
    
    print('LightSimulation finished')


print('Simulation started')
## --------------------------------------------------------------------
plt.figure()

# Position Eye
posEyeX = -10
plt.plot(posEyeX,0,'bo')
#plt.xlabel('Position x [mm]')

lenses = []
# Add lenses in the form
# lenses.append(Lense(<>,<>))

lenses.append(Lense(100, 1))

#lenses.append(Lense(-1000, 3))

#lenses.append(Lense(10000, 4))

# Define simulation photons
photon = Line([posEyeX,0], 1)

print(photon.x0)

dx =10;
#plt.plot([photon.x0[0],photon.x0[0]+dx],[photon.x0[1],photon.x0[1]+dx*photon.dir],'r')

lenses[0].photonSimulation(photon)

#lightSimulation(photon, lenses)





plt.show()

print('Simulation ended ')
