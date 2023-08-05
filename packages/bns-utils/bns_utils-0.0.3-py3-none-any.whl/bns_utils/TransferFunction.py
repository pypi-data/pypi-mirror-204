
import scipy.optimize 
import matplotlib.pyplot as plt
import numpy

class FOPDT:
    """
    Description: 
    This class implements a first order plus dead time (FOPDT) model
    The model is given by:
    y(t) = y0 + K*(1-exp(-t/tau))*(u(t-theta))
    where y0 is the initial condition, K is the gain, tau is the time constant, theta is the time delay and u(t) is the input
    the model is updated at a discrete time interval dt
    the model contains an optimise method which optimises the model parameters using the scipy.optimize.minimize function
    the model contains a simulate method which simulates the model for a given input and time vector
    the model contains a plot method which plots the results
    the model contains a generate_guess method which generates an initial guess for the model parameters using a least squares method
    this class assumes that at t=0 the input is zero and the output is zero

    Methods:
    __init__(self, K, tau, theta, y0, dt)
    update(self, u, t)
    setK(self, K)
    setTau(self, tau)
    setTheta(self, theta)
    setInitCond(self, y0)
    getK(self)
    getTau(self)
    getTheta(self)
    getInitCond(self)
    getOutput(self)
    Simultate(self,ts,us)
    Reset(self)
    __str__(self)
    objective(self,y_target,y_pred)
    generate_guess(self,us,ys,window_length)
    optimize(self,y,us,ts)
    plot(self,ts,us,ys,y_pred,u_delayed)

    Parameters:
    K: gain
    tau: time constant
    theta: time delay
    y0: initial condition
    dt: time step
    ts: time vector
    us: input vector
    ys: output vector
    y_pred: predicted output vector
    u_delayed: delayed input vector

    Example:
    import numpy as np
    import matplotlib.pyplot as plt
    from bns_utils.TransferFunction import FOPD
    # Generate a test signal
    ts = np.linspace(0,10,1000)
    us = np.sin(ts
    # Create a model
    model = FOPDT(1,1,1,0,0.01
    # Simulate the model
    ys,u_delayed = model.Simultate(ts,us
    # Plot the results
    model.plot(ts,us,ys,ys,u_delayed
    # Optimize the model parameters
    model.optimize(ys,us,ts)

   
    def __init__(self, K, tau, theta, y0, dt):
        self.K = K
        self.tau = tau
        self.theta = theta
        self.y0 = y0
        self.y = y0
        self.dt = dt
        
    """

    def update(self, u, t):
        # Update the state of the model given the input u and time t
        
        self.y = self.y + self.dt*((-(self.y-self.y0)+self.K*(u))/self.tau)
        return self.y
    
    def setK(self, K):
        # Set the value of the gain K
        self.K = K
        self.K_r = self.K*self.theta

    def setTau(self, tau):
        # Set the value of the time constant tau
        self.tau = tau
        self.tau_r = self.tau/self.theta

    def setTheta(self, theta):
        # Set the value of the time delay theta
        self.theta = theta

    def setInitCond(self, y0):
        # Set the initial condition
        self.y0 = y0

    def getK(self):
        # Return the value of the gain K
        return self.K
    
    def getTau(self):
        # Return the value of the time constant tau
        return self.tau
    
    def getTheta(self):
        # Return the value of the time delay theta
        return self.theta
    
    def getInitCond(self):
        # Return the initial condition
        return self.y
    
    def getOutput(self):
        return self.y
    
    def Simultate(self,ts,us):
        # Simulate the model for a given input and time vector
        ys = []
        u_delayed = []
        for  i in range(len(ts)):
            t = ts[i]
            if t <= self.theta:
                u = 0
                ys.append(self.update(u,t))
                u_delayed.append(u)
            else:
                u = us[i-int(self.theta/self.dt)]
                ys.append(self.update(u,t))
                u_delayed.append(u)
        self.y = self.y0
        return ys,u_delayed
    
    def Reset(self):
        # Reset the model
        self.y = self.y0

    def __str__(self):
        # Print the model parameters
        return "K = %f, tau = %f, theta = %f" % (self.K, self.tau, self.theta)
    
    def objective(self,y_target,y_pred):
        # Objective function
        return sum((y_target-y_pred)**2)
    
    def generate_guess(self,us,ys,window_length):
        # Generate an initial guess for the model parameters
        A = numpy.empty((0,window_length+1))
        for i in range(len(ys)-1):
            a_i = []
            a_i += [ys[i]]
            for j in range(window_length):
                if i-j<0:
                    a_i += [0]
                else:
                    a_i += [us[i-j]]
            a_i = numpy.array(a_i).reshape((1,-1))
            A = numpy.concatenate((A,a_i),axis=0)
        b = numpy.array(ys[1:]).reshape((-1,1))
        
        x = numpy.linalg.pinv(A)@b
        i = numpy.argmax(x[1:])
        alpha = x[0,0]
        beta = x[i+1,0]
        tau = self.dt/(1-alpha)
        gain = beta/(1-alpha)
        theta = i*self.dt
        return gain,tau,theta
    
    def optimize(self,y,us,ts):
        # Optimize the model parameters
        # Define the objective function
        def objective(x):
            self.setK(x[0])
            self.setTau(x[1])
            self.setTheta(x[2])
            y_pred,u_delayed = self.Simultate(ts,us)
            return self.objective(y,y_pred)
        
        # Initial guess
        x0 = self.generate_guess(us,y,100)
        
        # Optimize
        res = scipy.optimize.minimize(objective,x0,method='BFGS',options={'disp': True})
        
        # Set the optimal parameters
        self.setK(res.x[0])
        self.setTau(res.x[1])
        self.setTheta(res.x[2])
        
        # Return the optimal parameters
        return res.x
    
    def plot(self,ts,us,ys):
        # Plot the results
        plt.figure()
        #calculate the predicted output
        y_pred,u_delayed = self.Simultate(ts,us)
        plt.plot(ts,ys,label='y')
        plt.plot(ts,y_pred,label='y_pred')
        plt.legend()
        plt.show()

class Integrator:

    '''
    Documentation:
        This class implements a first order integrator

    Methods:
        update: update the state of the model given the input u and time t
        setK: set the value of the gain K
        setTheta: set the value of the time delay theta
        setInitCond: set the initial condition
        getK: return the value of the gain K
        getInitCond: return the initial condition

    Parameters:
        K: gain
        theta: time delay
        y0: initial condition
        dt: time step

    Example:
        model = Integrator(K, theta, y0, dt)
        model.update(u, t)
        model.setK(K)
        model.setTheta(theta)
        model.setInitCond(y0)
        model.getK()
        model.getInitCond()


    '''
       
    def __init__(self, K, theta, y0, dt):
        """
        Description:
            Constructor
        Parameters: 
            K: gain
            theta: time delay
            y0: initial condition
            dt: time step
        Returns:    
            None
        Example:    
            model = Integrator(K, theta, y0, dt)
        """
        self.K = K
        self.theta = theta
        self.y0 = y0
        self.y = y0
        self.dt = dt
        
    
    def update(self, u, t):
        """
        Description:
            Update the state of the model given the input u and time t
        Parameters:
            u: input
            t: time
        Returns:
            y: output
        Example:    
            y = model.update(u, t)
        """
        self.y = self.y + self.dt*(self.K*(u))
        return self.y
    
    def setK(self, K):
        """
        Description:
        Set the value of the gain K
        Parameters:
            K: gain
        Returns:
            None
        Example:    
            model.setK(K)
        """
        
        self.K = K

    def setTheta(self, theta):
        """
        Description:
            Set the value of the time delay theta
        Parameters:
            theta: time delay
        Returns:
            None
        Example:
            model.setTheta(theta)
        """
        self.theta = theta


    def setInitCond(self, y0):
        """
        Description:
            Set the initial condition
        Parameters:
            y0: initial condition
        Returns:
            None
        Example:
            model.setInitCond(y0)
        """
        self.y0 = y0

    def getK(self):
        """
        Description:
            Return the value of the gain K
        Parameters:
            None
        Returns:
            K: gain
        Example:
            K = model.getK()
        """
        return self.K
    
    def getInitCond(self):
        """
        Description:
            Return the initial condition
        Parameters:
            None
        Returns:
            y0: initial condition
        Example:
            y0 = model.getInitCond()
        """
        return self.y0
        
    
    def getOutput(self):
        """
        Description:
            Return the output
        Parameters:
            None
        Returns:
            y: output
        Example:
            y = model.getOutput()
        """

        return self.y
    
    
    def Simultate(self,ts,us):
        """
        Description:
            Simulate the model for a given input and time vector
        Parameters:
            ts: time vector
            us: input vector
        Returns:
            ys: output vector
            u_delayed: delayed input vector
        Example:
            ys,u_delayed = model.Simultate(ts,us)
        """
        ys = []
        u_delayed = []
        for  i in range(len(ts)):
            t = ts[i]
            if t <= self.theta:
                u = 0
                ys.append(self.update(u,t))
                u_delayed.append(u)
            else:
                u = us[i-int(self.theta/self.dt)]
                ys.append(self.update(u,t))
                u_delayed.append(u)
        return ys,u_delayed
    
    def Reset(self):
        """
        Description:
            Reset the model to the initial condition
        Parameters:
            None
        Returns:
            None
        Example:
            model.Reset()
        """
        # Reset the model
        self.y = self.y0

    def __str__(self):
        """
        Description:
            Print the model parameters
        Parameters:
            None
        Returns:
            None
        Example:
            model.__str__()
        """
        # Print the model parameters: the gain and the time delay
        return "K = %f" % (self.K)
    
    def objective(self,y_target,y_pred):
        """
        Description:
            Calculate the objective function
        Parameters:
            y_target: target output
            y_pred: predicted output
        Returns:
            sum((y_target-y_pred)**2): objective function
        Example:
            J = model.objective(y_target,y_pred)
        """
        # Objective function
        return sum((y_target-y_pred)**2)
    
    def optimize(self,y,us,ts):
        """
        Description:
            Optimize the model parameters
        Parameters:
            y: target output
            us: input vector
            ts: time vector
        Returns:
            res.x: optimal parameters
        Example:
            res.x = model.optimize(y,us,ts)
        """
        # Optimize the model parameters
        # Define the objective function
        def objective(x):
            self.setK(x[0])
            self.setTheta(x[1])
            y_pred,u_delayed = self.Simultate(ts,us)
            return self.objective(y,y_pred)
        
        # Initial guess
        x0 = [self.K,self.theta]
        
        # Optimize
        res = scipy.optimize.minimize(objective,x0,method='BFGS',options={'disp': True})
        
        # Set the optimal parameters
        self.setK(res.x[0])
        
        # Return the optimal parameters
        return res.x
    
    # create destructor
    def __del__(self):
        """
        Description:
            Destructor
        Parameters:
            None
        Returns:
            None
        Example:
            model.__del__()
        """
        #erase all the variables
        self.K = None
        self.theta = None
        self.y0 = None
        self.y = None
        self.dt = None
        
        # Clean up any resources used by the object
        pass

class MIMO:
    """
    Description:
        This class is used to generate the MIMO model of the system.
    Parameters:
        Us: The input matrix of the system. - numpy.ndarray, shape = (samples, n_inputs)
        Ys: The output matrix of the system. - numpy.ndarray shape = (samples, n_outputs)
        ts: The time vector of the system. - numpy.ndarray shape = (samples,)
        ModelMatrix: The model matrix of the system. - numpy.ndarray shape = (n_outputs, n_inputs)
    Returns:
        None
    """

    def __init__(self, Us, Ys, ts, ModelMatrix):
        """
        Description:
            This method is used to initialize the class.
        Parameters:
            Us: The input matrix of the system.
            Ys: The output matrix of the system.
            ts: The time vector of the system.
            ModelMatrix: The model matrix of the system.
        Returns:
            None
        """

        self.Us = Us
        self.Ys = Ys
        self.ts = ts
        self.ModelMatrix = ModelMatrix
        self.dt = ts[1]-ts[0]
    
    def get_dt(self):
        """
        Description:
            This method is used to get the dt of the system.
        Parameters:
            None
        Returns:
            dt: The dt of the system.
        """
        return self.dt

    def GenerateGuessParams(self,window_length, ModelMatrix, U, Ys):
        """
        Description:
            This method is used to generate the initial guess of the parameters.
        Parameters:
            window_length: The window length of the system.
            ModelMatrix: The model matrix of the system.
            U: The input matrix of the system.
            Ys: The output matrix of the system.
        Returns:
            parameter_guesses: The initial guess of the parameters.
        """
        #store the window length
        self.window_length = window_length
        #create a dictionary to store the guesses
        parameter_guesses = {}
        
        for ny in range(numpy.shape(Ys)[1]):
            ys = Ys[:,ny]         
            A = numpy.empty((0,numpy.shape(U)[1]*window_length+1)) # A is the input matrix
            for i in range(len(ys)-1):
                a_i = []
                a_i += [ys[i]]
                for nu in range(numpy.shape(U)[1]):
                    us = U[:,nu]
                    for j in range(window_length):
                        if i-j<0:
                            a_i += [0]
                        else:
                            a_i += [us[i-j]]
                a_i = numpy.array(a_i).reshape((1,-1))
                A = numpy.concatenate((A,a_i),axis=0)
            b = numpy.array(ys[1:]).reshape((-1,1)) # b is the output vector shifted by one
            lamb = 1e-3 # regularization parameter
            x = numpy.linalg.pinv(A.T @ A + lamb * numpy.eye(A.shape[1]))@A.T @b #solution of the least squares problem with regularization
            gains, taus, thetas = [], [], []
            for k in range(U.shape[1]):
                i = numpy.argmax(x[1+k*window_length : (k+1)*window_length+1])
                alpha = x[k*window_length, 0]
                beta = x[k*window_length+i+1, 0]
                tau = self.dt / (1 - alpha) # tau = theta / (1 - alpha)
                gain = beta*tau/self.dt
                theta = i * self.dt
                gains.append(gain)
                taus.append(tau)
                thetas.append(theta)
            
            
            A_2 = numpy.empty((0,2*numpy.shape(U)[1]))
            for i in range(len(ys)-1):
                a_i_2 = []
                for nu in range(numpy.shape(U)[1]):
                    a_i_2 += [ys[i]]
                for nu in range(numpy.shape(U)[1]):
                    us = U[:,nu]
                    
                    theta = thetas[nu]+self.dt
                    if i-theta<0:
                        a_i_2 += [0]
                    else:
                        a_i_2 += [us[i-int(theta/self.dt)]]
                a_i_2 = numpy.array(a_i_2).reshape((1,-1))
                A_2 = numpy.concatenate((A_2,a_i_2),axis=0)
            b_2 = numpy.array(ys[1:]).reshape((-1,1)) # b is the output vector shifted by one
            lamb_2 = 1e-3 # regularization parameter
            x_2 = numpy.linalg.pinv(A_2.T @ A_2 + lamb_2 * numpy.eye(A_2.shape[1]))@A_2.T @b_2 #solution of the least squares problem with regularization
            alphas = []
            #append the first nu values of x_2 to alphas
            for k in range(U.shape[1]):
                alphas.append(x_2[k,0])
                
            # calculate the gains and taus

            gains_2, taus_2 = [], []
            N_U = U.shape[1]

            # nu*y(k+1) = alpha_1*y(k) + alpha_2*y(k) + ... + alpha_nu*y(k) + beta_1*u1(k-theta_1) + beta_2*u2(k-theta2) + ... + beta_nu*nu(k-theta_nu)
            # nu*y(k+1) = (1-dt/tau_1)*y(k) + (1-dt/tau_2)*y(k) + ... + (1-dt/tau_nu)*y(k) + dt*gain_1*u1(k-theta_1) + dt*gain_2*u2(k-theta2) + ... + dt*gain_nu*nu(k-theta_nu)

            for k in range(U.shape[1]):

                if ModelMatrix[ny,k] == 'FOPDT':
                    alpha = alphas[k]
                    tau = self.dt / (1 - alpha*(N_U)) # tau = theta / (1 - alpha)
                    gain = x_2[k+U.shape[1],0]*tau/self.dt
                    theta = thetas[k] + self.dt
                    gains_2.append(gain)
                    taus_2.append(tau)

                elif ModelMatrix[ny,k] == 'Integrator':
                    alpha = alphas[k]
                    gain = x_2[k+U.shape[1],0]
                    theta = thetas[k] + self.dt
                    gains_2.append(gain)
                    taus_2.append(0)

                    

            # append the guesses to the dictionary
            for nu in range(numpy.shape(U)[1]):
                if ModelMatrix[ny,nu] == 'FOPDT':
                    gain = gains_2[nu]
                    tau = taus_2[nu]
                    theta = thetas[nu]+self.dt
                    parameter_guesses[f'G{ny+1}{nu+1}'] = [gain,tau,theta]
                    
                elif ModelMatrix[ny,nu] == 'Integrator':
                    gain = gains_2[nu]
                    tau = taus_2[nu]
                    theta = thetas[nu]+self.dt
                    parameter_guesses[f'G{ny+1}{nu+1}'] = [gain,theta]
            

            self.parameter_guesses = parameter_guesses

        return self.parameter_guesses
    
    # use the generate guess function to generate guesses for the parameters
    #using the generated guess points create FOPDT models for each output/input pair 

    def GenerateGuessFOPDTModelsResponse(self,ts, Us , Ys):
        """
        Description:
            Generate the response of the FOPDT models using the generated guesses for the parameters
        Parameters:
            ts: time vector
            Us: input matrix
            Ys: output matrix
        Returns:
            Y_matrix: matrix of the responses of the FOPDT models
        """
        #create a dictionary to store the guesses
        parameter_guesses = self.GenerateGuessParams(self.window_length, self.ModelMatrix, self.Us, self.Ys)
        #create a dictionary to store the models

        Y_matrix = numpy.empty(numpy.shape(Ys))
        
        for ny in range(numpy.shape(Ys)[1]):

            y_final = numpy.zeros(len(ts))
            
            for nu in range(numpy.shape(Us)[1]):

                if self.ModelMatrix[ny,nu] == 'FOPDT':
                
                    # access the guesses for the parameters
                    Gain,tau,theta = parameter_guesses[f'G{ny+1}{nu+1}']
                    #create a model for each output/input pair
                    model_io = FOPDT(Gain,tau,theta,0,self.dt)

                    ysim,u_delayed = model_io.Simultate(ts = self.ts, us = self.Us[:,nu])
                    ysim = numpy.array(ysim)

                    model_io.__del__()

                else:

                    Gain,theta = parameter_guesses[f'G{ny+1}{nu+1}']
                    #create a model for each output/input pair
                    model_io = Integrator(Gain,theta,0,self.dt)

                    ysim,u_delayed = model_io.Simultate(ts = self.ts, us = self.Us[:,nu])
                    ysim = numpy.array(ysim)

                    model_io.__del__()
                

                y_final += ysim

            Y_matrix[:,ny] = y_final

        return Y_matrix
    

    
    def Optimize_outputi(self,ts,Us,ny):
        """
        Description:
            Optimize the parameters of the FOPDT models for each output/input pair
        Parameters:
            ts: time vector
            Us: input matrix
            ny: output index
        Returns:
            x: optimized parameters
        """

        def Calculate_objective(x):
            """
            Description:
                Calculate the objective function
            Parameters:
                x: parameters
            Returns:
                objective: objective function
            """

            y_final = numpy.zeros(len(ts))

            for nu in range(numpy.shape(Us)[1]):
                
                if self.ModelMatrix[ny,nu] == 'FOPDT':
                
                    # access the parameters from the vector x
                    Gain,tau,theta = x[nu*3],x[nu*3+1],x[nu*3+2]
                    #create a model for each output/input pair
                    model_io = FOPDT(Gain,tau,theta,0,self.dt)

                    ysim,u_delayed = model_io.Simultate(ts = self.ts, us = self.Us[:,nu])

                    ysim = numpy.array(ysim)

                else:

                    Gain,theta = x[nu*3],x[nu*3+1]
                    #create a model for each output/input pair
                    model_io = Integrator(Gain,theta,0,self.dt)

                    ysim,u_delayed = model_io.Simultate(ts = self.ts, us = self.Us[:,nu])

                    ysim = numpy.array(ysim)

                    model_io.__del__()

                y_final += ysim

            obj = 0
            y_true = self.Ys[:,ny]
            for i in range(len(y_true)):
                obj += (y_true[i] - y_final[i])**2

            return obj
        
        # create a vector of initial guesses for the parameters
        x0 = []
        for nu in range(numpy.shape(Us)[1]):

            if self.ModelMatrix[ny,nu] == 'FOPDT':
                Gain,tau,theta = self.parameter_guesses[f'G{ny+1}{nu+1}']
                x0 += [Gain,tau,theta]

            else:
                Gain,theta = self.parameter_guesses[f'G{ny+1}{nu+1}']
                x0 += [Gain,theta,0]

        x0 = numpy.array(x0)

        # optimize the objective function
        res = scipy.optimize.minimize(Calculate_objective, x0, method='BFGS', options={'disp': True})
        print('Hoorah!')
        # create a dictionary to store the optimized parameters
        optimized_params = {}
        for nu in range(numpy.shape(Us)[1]):
            if self.ModelMatrix[ny,nu] == 'FOPDT':

                optimized_params[f'G{ny+1}{nu+1}'] = [res.x[nu*3],res.x[nu*3+1],res.x[nu*3+2]]

            else:
                    
                optimized_params[f'G{ny+1}{nu+1}'] = [res.x[nu*3],res.x[nu*3+1]]

        self.optimized_params = optimized_params
        return optimized_params
    

    # use the optimized parameters to create FOPDT models for each output/input pair and simulate the response
    def GenerateFOPDTModelsResponse(self,ts, Us , Ys):
        """
        Description:
            Generate the responses of the FOPDT models
        Parameters:
            ts: time vector
            Us: input matrix
            Ys: output matrix
        Returns:
            Y_matrix: matrix of the responses of the FOPDT models
        """
        
        #create a dictionary to store the models

        Y_matrix = numpy.empty(numpy.shape(Ys))
        
        for ny in range(numpy.shape(Ys)[1]):

            y_final = numpy.zeros(len(ts))
            
            for nu in range(numpy.shape(Us)[1]):

                if self.ModelMatrix[ny,nu] == 'FOPDT':
                
                    # access the guesses for the parameters
                    Gain,tau,theta = self.optimized_params[f'G{ny+1}{nu+1}']
                    #create a model for each output/input pair
                    model_io = FOPDT(Gain,tau,theta,0,self.dt)

                    ysim,u_delayed = model_io.Simultate(ts = self.ts, us = self.Us[:,nu])
                    ysim = numpy.array(ysim)
                    model_io.__del__()
                
                else:

                    Gain,theta = self.optimized_params[f'G{ny+1}{nu+1}']
                    #create a model for each output/input pair
                    model_io = Integrator(Gain,theta,0,self.dt)

                    ysim,u_delayed = model_io.Simultate(ts = self.ts, us = self.Us[:,nu])
                    ysim = numpy.array(ysim)
                    model_io.__del__()

                
                y_final += ysim

            Y_matrix[:,ny] = y_final

        return Y_matrix
    
    def Optimizer(self,ts,Us,Ys):
        """
        Description:
            Optimize the parameters of the FOPDT models for each output/input pair
        Parameters:
            ts: time vector
            Us: input matrix
            Ys: output matrix
        Returns:
            optimized_params: optimized parameters
        """
        # create a dictionary to store the optimized parameters
        optimized_params = {}
        for ny in range(numpy.shape(Ys)[1]):
            optimized_params.update(self.Optimize_outputi(ts,Us,ny))
        self.optimized_params = optimized_params
        return optimized_params
    
    def Simulate_Optimized_params(self,ts,Us,Ys):
        """
        Description:
            Simulate the response of the system using the optimized parameters
        Parameters:
            ts: time vector
            Us: input matrix
            Ys: output matrix
        Returns:
            Y_matrix: matrix of the responses of the FOPDT models
        """
        
        Y_matrix = numpy.empty(numpy.shape(Ys))

        for ny in range(numpy.shape(Ys)[1]):

            y_final = numpy.zeros(len(ts))
            
            for nu in range(numpy.shape(Us)[1]):

                if self.ModelMatrix[ny,nu] == 'FOPDT':
                
                    # access the guesses for the parameters
                    Gain,tau,theta = self.optimized_params[f'G{ny+1}{nu+1}']
                    #create a model for each output/input pair
                    model_io = FOPDT(Gain,tau,theta,0,self.dt)

                    ysim,u_delayed = model_io.Simultate(ts = self.ts, us = self.Us[:,nu])
                    ysim = numpy.array(ysim)
                    model_io.__del__()
                
                else:

                    Gain,theta = self.optimized_params[f'G{ny+1}{nu+1}']
                    #create a model for each output/input pair
                    model_io = Integrator(Gain,theta,0,self.dt)

                    ysim,u_delayed = model_io.Simultate(ts = self.ts, us = self.Us[:,nu])
                    ysim = numpy.array(ysim)
                    model_io.__del__()

                
                y_final += ysim

            Y_matrix[:,ny] = y_final



        return Y_matrix
    

                    

                    
