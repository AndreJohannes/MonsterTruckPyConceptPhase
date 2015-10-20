import math, numpy
import pdb

class Vehicle:

	def __init__(self, objects):
		self.objects = objects
		self.throttle = 0
		# car geometry, should be stored somewhere else eventually
		# currently the centre of the car is at  98/58; the size of the entire car is (196,116)
		self.center_of_mass = [0, 0] # This is the center of mass with respect to the geometrical centre of the vehicle
		self.position_wheel_rear = [-46,24] # This is the positions with respect to the geometrical centre 
		self.position_wheel_front = [59,24]  # This is the positions with respect to the geometrical centre
		self.CM_to_wheel_front = [self.position_wheel_front[0]-self.center_of_mass[0], self.position_wheel_front[1]-self.center_of_mass[1]] 	
		self.CM_to_wheel_rear = [self.position_wheel_rear[0]-self.center_of_mass[0], self.position_wheel_rear[1]-self.center_of_mass[1]] 

	def get_geometry(self):
		return self.center_of_mass, self.position_wheel_front, self.position_wheel_rear

	def get_positions(self):
		sin = math.sin(self.angle);
		cos = math.cos(self.angle);
		front_x =  self.center_of_mass[0]+self.position_wheel_front[0]
		front_y =  self.center_of_mass[1]+self.position_wheel_front[1]
		rear_x =  self.center_of_mass[0]+self.position_wheel_rear[0]
		rear_y =  self.center_of_mass[1]+self.position_wheel_rear[1]
		return  self.position, \
			[self.position[0]+cos*front_x+sin*front_y, self.position[1]+cos*front_y-sin*front_x], \
			[self.position[0]+cos*rear_x+sin*rear_y, self.position[1]+cos*rear_y-sin*rear_x]

	def get_suspensions(self, state):
		ground = 300
		position_x = state[0]
		position_y = state[1]
		rad = state[4]
		sin = math.sin(rad);
		cos = math.cos(rad);
		#position_wheel_front_x = position_x + cos*self.CM_to_wheel_front[0] + sin*self.CM_to_wheel_front[1]
		position_wheel_front_y = position_y + cos*self.CM_to_wheel_front[1] - sin*self.CM_to_wheel_front[0]
		#position_wheel_rear_x = position_x + cos*self.CM_to_wheel_rear[0] + sin*self.CM_to_wheel_rear[1]
		position_wheel_rear_y = position_y + cos*self.CM_to_wheel_rear[1] - sin*self.CM_to_wheel_rear[0]
		dist_front = (ground-position_wheel_front_y) if position_wheel_front_y > ground else 0 
		dist_rear = (ground-position_wheel_rear_y) if position_wheel_rear_y > ground else 0
		dist_front_x = -sin * dist_front
		dist_front_y = cos *dist_front
		dist_rear_x = -sin * dist_rear 
		dist_rear_y = cos * dist_rear 
		return [dist_front_x, dist_front_y],[dist_rear_x, dist_rear_y]

	def get_function(self, state):
		position_x = state[0]; position_y = state[1]
		velocity_x = state[2]; velocity_y = state[3]
		rad = state[4]; angular_velocity = state[5]
		sin = math.sin(rad); cos = math.cos(rad);
		# Next we calculate the position of the centers of the front and rear wheel
		position_wheel_front_x = position_x + cos*self.CM_to_wheel_front[0] + sin*self.CM_to_wheel_front[1]
		position_wheel_front_y = position_y + cos*self.CM_to_wheel_front[1] - sin*self.CM_to_wheel_front[0]
		position_wheel_rear_x = position_x + cos*self.CM_to_wheel_rear[0] + sin*self.CM_to_wheel_rear[1]
		position_wheel_rear_y = position_y + cos*self.CM_to_wheel_rear[1] - sin*self.CM_to_wheel_rear[0]
		
		objects_front = self.objects.get_objects(position_wheel_front_x, position_wheel_front_y)
		objects_rear = self.objects.get_objects(position_wheel_rear_x, position_wheel_rear_y)
		
		force_front_x=0; force_font_y=0; touch_front = False; 
		for object_front in objects_front:
			ext = object_front[0]
			n = object_front[1]
			touch_front = True
			force_front_x += 5 * ext * n[0]
			force_front_y += 5 * ext * n[1] 
		force_rear_x=0; force_front_y=0; touch_rear = False;
		for object_rear in objects_rear
			ext = object_rear[0]
			n = objects_rear[1]
			touch_rear = True
			force_rear_x += 5 * ext *n[0]
			force_rear_y += 5 * ext *n[1]

		force_g =  5 # add g-force
		force_friction = -(0.1 + (0.2 if  position_wheel_front_y > ground else 0) +(0.2 if position_wheel_rear_y > ground else 0))*velocity_y 
		force_y = force_g+force_front_x+force_rear_x
		force_x = force_front_y + force_rear_y
		force_x += (self.throttle -0.1*velocity_x)  if (position_wheel_rear_y +10 > ground) else -0.1*velocity_x
		torque =  \
			force_front_x*(-cos*self.CM_to_wheel_front[1]+sin*self.CM_to_wheel_front[0]) + \
			(force_rear+force_x)*(cos*self.CM_to_wheel_rear[1]-sin*self.CM_to_wheel_rear[0]) 
	 

		return numpy.array([velocity_x, velocity_y, force_x, force_y, angular_velocity , 0.00003*torque-0.08*angular_velocity])

	def set_throttle(self, throttle):
		self.throttle = throttle;