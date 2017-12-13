"""
Lens simulation using python

EPFL - Product Devlopement

Author: Huber Lukas
Date: 2017/11/02

"""
## Import libraries
import numpy as np #math library
import matplotlib.pyplot as plt # figure plotting
from math import cos,sin,asin,acos ,tan,atan2, sqrt, pi

refractionIndex_air = 1.000277

class Lens():
    # Geometrical properties
    widthMin = 0.1 # [mm]
    
    # Visulazation
    N_points = 10 # number of datapoints to plot each side

    def __init__(self, corr, posx, type='default'):
        # Correction coefficient
        # Position in [mm], where the eye is at zero
        
        self.corr = corr
        
        self.posx = -posx # possible? convert to [m]
 
        self.convex = np.sign(corr) #

        if(type  == 'eye'):
            self.widthBord = 0 # [mm]

            # Fraction Coefficient
            self.refractionIndex = 1.0 # Different.. Find out.

            self.rad_lens = 15
                
        
        else:
            #print(type + ' created...')
            self.widthBord = 2*2 # [mm]

            # Fraction Coefficient
            self.refractionIndex = 1.47 # Glycerol
            
            self.rad_lens  = 30/2  # [mm]
        
        if self.convex>0:
            self.rad_curve = corr
            self.phi_lens = asin(self.rad_lens/self.rad_curve)

            self.pos0 = [self.posx - self.rad_curve*cos(self.phi_lens) + 0.5*self.widthBord ,
                         self.posx + self.rad_curve*cos(self.phi_lens) - 0.5*self.widthBord ]

            plt.plot([self.pos0[0]+self.rad_curve*cos(-self.phi_lens+self.phi_lens*2/self.N_points*i)
                  for i in range(self.N_points+1)],
                 [self.rad_curve*sin(-self.phi_lens + self.phi_lens*2/self.N_points*i)
                  for i in range(self.N_points+1)],'k')

            plt.plot([self.pos0[1]-self.rad_curve*cos(-self.phi_lens+self.phi_lens*2/self.N_points*i)
                   for i in range(self.N_points+1)],
                  [self.rad_curve*sin(-self.phi_lens + self.phi_lens*2/self.N_points*i)
                   for i in range(self. N_points+1)],'k')

            # Plot lower boundary
            plt.plot([self.pos0[1]-self.rad_curve*cos(-self.phi_lens),
                      self.pos0[0]+self.rad_curve*cos(-self.phi_lens)],
                     [self.rad_curve*sin(-self.phi_lens),
                      self.rad_curve*sin(-self.phi_lens)],
                     'k')
            # Plot upper boundary
            plt.plot([self.pos0[1]-self.rad_curve*cos(self.phi_lens),
                      self.pos0[0]+self.rad_curve*cos(self.phi_lens)],
                     [self.rad_curve*sin(self.phi_lens),
                      self.rad_curve*sin(self.phi_lens)],
                     'k')
            
        elif self.convex == 0:
            print('flat plate detected')
            
        else:
            self.rad_curve = -corr
            self.phi_lens = asin(self.rad_lens/self.rad_curve)
            
            self.pos0 = [self.posx-(self.widthMin/2+self.rad_curve),
                         self.posx+(self.widthMin/2+self.rad_curve)]

            dPhi = self.phi_lens*2/self.N_points # angle iteration for plot
            
            plt.plot([self.pos0[0]+self.rad_curve*cos(-self.phi_lens+dPhi*i)
                  for i in range(self.N_points+1)],
                 [self.rad_curve*sin(-self.phi_lens + dPhi*i)
                  for i in range(self.N_points+1)],'k')

            plt.plot([self.pos0[1]-self.rad_curve*cos(-self.phi_lens+dPhi*i)
                   for i in range(self.N_points+1)],
                  [self.rad_curve*sin(-self.phi_lens + dPhi*i)
                   for i in range(self. N_points+1)],'k')

            # Plot lower boundary
            plt.plot([self.pos0[1]-self.rad_curve*cos(-self.phi_lens),
                      self.pos0[0]+self.rad_curve*cos(-self.phi_lens)],
                     [self.rad_curve*sin(-self.phi_lens),
                      self.rad_curve*sin(-self.phi_lens)],
                     'k')
            # Plot upper boundary
            plt.plot([self.pos0[1]-self.rad_curve*cos(self.phi_lens),
                      self.pos0[0]+self.rad_curve*cos(self.phi_lens)],
                     [self.rad_curve*sin(self.phi_lens),
                      self.rad_curve*sin(self.phi_lens)],
                     'k')
        if(type == 'eye'):
            eyeRadius = 30
            #print(self.rad_lens/eyeRadius)
            phiEye = asin(self.rad_lens/eyeRadius)
            eyeCenter = self.posx + eyeRadius*cos(phiEye)

            N_eyeSim = 20 # resolution to draw the eye
            
            dphi = 2*(pi-phiEye)/(N_eyeSim-1)
            plt.plot([eyeCenter-eyeRadius*cos(phiEye + dphi*i)
                      for i in range(N_eyeSim)],                     
                     [eyeRadius*sin(phiEye + dphi*i)
                      for i in range(N_eyeSim)],'r')
    def getVolume(self):
        # Return in ml / cm^2
        V_varry = self.rad_curve**2 * pi * ( 2/3*self.rad_curve - self.rad_curve*cos(self.phi_lens)  + 1/3 *self.rad_curve*cos(self.phi_lens)**3 )

        V_middle =  pi * (self.widthBord *(self.rad_lens)**2)
        
        # Return total volume in [ml] == [cm3]
        return 0.001*(2*V_varry + V_middle) 
    
        

    def photonSimulation(self, photon):
        # Extract line parameters
        a = photon.dir
        b = photon.x0[1]-a*photon.x0[0]

        # Extract lens parameters
        x0 = self.pos0[1]
        r = self.rad_curve

        # Find point of intersection with the lens
        a1 = 1+a**2
        b1 = -2*a*b - 2*a**2*x0
        c1 = a**2*x0**2 + 2*a*b*x0 + b**2 - r**2

        #if self.convex > 0:
        dx = (-b1 + sqrt(b1**2-4*a1*c1))/(2*a1)
        #else:
        # dx = (-b1 - sqrt(b1**2-4*a1*c1))/(2*a1)
            
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

        # Extract lens parameters
        x0 = self.pos0[0]
        r = self.rad_curve

        # Find point of intersection
        a1 = 1+a**2
        b1 = 2*a*b + 2*a**2*x0
        c1 = a**2*x0**2 + 2*a*b*x0 + b**2 - r**2

        #if self.convex > 0:      
        dx = (-b1 + sqrt(b1**2-4*a1*c1))/(2*a1)
        #else:
        #dx = (-b1 - sqrt(b1**2-4*a1*c1))/(2*a1)

        x_out = x0+dx
        y_out = a*x_in+b

        plt.plot([x_in,x_out],[y_in,y_out], 'm')

        phi_out = atan2(y_out,dx)
        theta1_abs_out = atan2(a,1)

        if self.convex:
            theta1_rel_out = theta1_abs_out - phi_out
        else:
            theta1_rel_out = theta1_abs_out + phi_out



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


def lastArraySimu(lightOut, dx = 40):
    a = lightOut.dir
    b = lightOut.x0[1]- a*lightOut.x0[0]

    yLim = lenss[0].rad_lens*1.05

    #dx = 100
    
    plt.plot([lightOut.x0[0],lightOut.x0[0]+dx],[lightOut.x0[1],lightOut.x0[1]+dx*a],'m')

def lightSimulation(incomingLight, lenss):
    for p in range(len(incomingLight)):
        photon = incomingLight[p]
        for i in range(len(lenss)): # 
            photon = lenss[i].photonSimulation(photon)

        # Intersection with horizontal
        lastArraySimu(photon, 50.)

    #print('LightSimulation finished')

    
def CreateObjectsArrays(pos, lensDistMax):
    safetyMargin = 0.4
    rad_lens = 30
    nArrays = 7

    photons = []
    #print(pos)
    
    angMax = atan2(rad_lens, pos[0]-lensDistMax)*safetyMargin

    #print(angMax)
    dAng = 2*angMax/(nArrays-1)
    
    for i in range(nArrays):
        photons.append(Line([-pos[0],pos[1]], tan(dAng*i-angMax)))
    
    return photons

################################################################################
#
# MODIFY here
#

print('Simulation started')
print('')
## --------------------------------------------------------------------

plt.figure()
plt.subplot(2,1,1)


# Position Eye
lenss = []
# Add lenss in the form
# lenss.append(Lens(<>,<>))
lenss.append(Lens(58, 25))
print('Lens1 volume is ',  round(lenss[0].getVolume(),2), 'ml.')
# Simulate Eye
lenss.append(Lens(50, 0, 'eye'))


# Define simulation photons
photonsClose = CreateObjectsArrays([200,0], 100)
#photonsClose = CreateObjectsArrays([100000,0], 100)

# Simulate
lightSimulation(photonsClose, lenss)

plt.xlim([-120, 60])



# Second scenario - lense far
plt.subplot(2,1,2)

# Position Eye

lenss = []
# Add lenss in the form
# lenss.append(Lens(<>,<>))
lenss.append(Lens(70, 25))
print('Lens2 volume is ',  round(lenss[0].getVolume(),2), 'ml.')
# Simulate Eye
lenss.append(Lens(50, 0, 'eye'))


# Define simulation photons
photonsClose = CreateObjectsArrays([100000,0], 100)

# Simulate
lightSimulation(photonsClose, lenss)

plt.xlim([-120, 60])

# Display plot
plt.xlabel('Distance [mm]')
plt.show()

print('')
print('Simulation ended ')
