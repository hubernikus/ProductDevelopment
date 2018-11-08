"""
Lense simulation using python

EPFL - Product Devlopement

Author: Huber Lukas
Date: 2017/11/02

"""
## Import libraries
import numpy as np #math library
import matplotlib.pyplot as plt # figure plotting
from math import cos,sin,asin,acos ,tan,atan2, sqrt, pi

refractionIndex_air = 1.000277

class Lense():
    # Geometrical properties
    widthMin = 0.1 # [mm]
    rad_lens  = 30  # [mm]

    # Visulazation
    N_points = 10 # number of datapoints to plot each side

    def __init__(self, corr, posx):
        # Correction coefficient
        # Position in [mm], where the eye is at zero
        
        self.corr = corr
        
        self.posx = -posx # possible? convert to [m]

        self.convex = np.sign(corr) #

        
        # Fraction Coefficient
        self.refractionIndex = 1.47 # Glycerol

        
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
de            
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
                # Extract line parameters
        a = photon.dir
        b = photon.x0[1]-a*photon.x0[0]

        # Extract lense parameters
        x0 = self.pos0[1]
        r = self.rad_curve

        # Find point of intersection with the lense
        a1 = 1+a**2
        b1 = -2*a*b - 2*a**2*x0
        c1 = a**2*x0**2 + 2*a*b*x0 + b**2 - r**2

        dx = (-b1 + sqrt(b1**2-4*a1*c1))/(2*a1)

        x_in = x0-dx
        y_in = a*x_in+b

        plt.plot([photon.x0[0],x_in],[photon.x0[1],y_in],'m')

        # Refraction of the light beam
        phi_in = atan2(y_in,dx)
        theta1_abs_in = atan2(a,1)
        theta1_rel_in = theta1_abs_in + phi_in

        theta2_rel_in = asin(refractionIndex_air/self.refractionIndex*sin(theta1_rel_in))
        theta2_abs_in = theta2_rel_in-phi_in

        dr = 2
        plt.plot([self.pos0[1]-(r-dr)*cos(phi_in), self.pos0[1]-(r+dr)*cos(phi_in)],
            [(r-dr)*sin(phi_in), (r+dr)*sin(phi_in)],'k--')


        # Extract line parameters
        a = theta2_abs_in
        b = y_in-a*x_in

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

        plt.plot([x_in,x_out],[y_in,y_out], 'm')

        phi_out = atan2(y_out,dx)
        theta1_abs_out = atan2(a,1)
        if self.convex<0:
            theta1_rel_out = theta1_abs_out + phi_out
        else:
            theta1_rel_out = theta1_abs_out - phi_out

        theta2_rel_out = asin(self.refractionIndex/refractionIndex_air*sin(theta1_rel_out))
        theta2_abs_out = theta2_rel_out + phi_out

                    # plot normal (for defraction visualization)
        plt.plot([self.pos0[0]+(r-dr)*cos(phi_out), self.pos0[0]+(r+dr)*cos(phi_out)],
                 [(r-dr)*sin(phi_out), (r+dr)*sin(phi_out)],'k--')

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


def lastArraySimu(lightOut):
    a = lightOut.dir
    b = lightOut.x0[1]- a*lightOut.x0[0]

    yLim = Lense.rad_lens*1.05

    if b > 0:
        dx = (yLim-lightOut.x0[1])/a
    elif b < 0:
        dx = (-yLim-lightOut.x0[1])/a
    else:
        dx = 10 # [mm] - plot for some distance...

    maxDist = 20 # maximal desired display in x direction
    dx = min(maxDist, abs(dx))
    
    dx = 80
    
    plt.plot([lightOut.x0[0],lightOut.x0[0]+dx],[lightOut.x0[1],lightOut.x0[1]+dx*a],'m')
    

def lightSimulation(incomingLight, lenses):
    for p in range(len(incomingLight)):
        photon = incomingLight[p]
        for i in range(len(lenses)): # 
            photon = lenses[i].photonSimulation(photon)

            # Intersection with horizontal
        lastArraySimu(photon)

    #print('LightSimulation finished')

    
def CreateObjectsArrays(pos, lenseDistMax):
    safetyMargin = 0.4
    rad_lense = 30
    nArrays = 7

    photons = []
    print(pos)
    
    angMax = atan2(rad_lense, pos[0]-lenseDistMax)*safetyMargin

    print(angMax)
    dAng = 2*angMax/(nArrays-1)
    
    for i in range(nArrays):
        photons.append(Line([-pos[0],pos[1]], tan(dAng*i-angMax)))
    
    return photons

################################################################################
#
# MODIFY here
#

print('Simulation started')
## --------------------------------------------------------------------

plt.figure()
plt.subplot(2,1,1)


# Position Eye
posEyeX = 50
plt.plot(posEyeX,0,'bo')


lenses = []
# Add lenses in the form
# lenses.append(Lense(<>,<>))
#lenses.append(Lense(1000, 100))
lenses.append(Lense(120, 50))
#lenses.append(Lense(1000, 30))
lenses.append(Lense(200, 30))
# Simulate Eye
lenses.append(Lense(50, 0))


# Define simulation photons
photonsClose = CreateObjectsArrays([200,0], 100)
#photonsClose = CreateObjectsArrays([100000,0], 100)

# Simulate
lightSimulation(photonsClose, lenses)

plt.xlim([-120, 80])

# TODOOOO: use in supblots, far vs close

plt.subplot(2,1,2)

# Position Eye
plt.plot(posEyeX,0,'bo')
#plt.xlabel('Position x [mm]')

lenses = []
# Add lenses in the form
# lenses.append(Lense(<>,<>))
lenses.append(Lense(-300, 50))
#lenses.append(Lense(500, 80))
lenses.append(Lense(200, 30))
#lenses.append(Lense(500, 10))

# Simulate Eye
lenses.append(Lense(70, 0))


# Define simulation photons
photonsClose = CreateObjectsArrays([100000,0], 100)

# Simulate
lightSimulation(photonsClose, lenses)

plt.xlim([-120, 80])

# Display plot
plt.xlabel('Position x [mm]')
plt.show()

print('Simulation ended ')
