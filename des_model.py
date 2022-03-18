class DES_model:
    ''' Discrete event system model.
    '''

    def __init__(self, d, tu, tl, nt, v, L):
        ''' Construct a discrete event system model.

        Args:
            d (numpy.array): distance from port to terminal.
            tu (numpy.array): unloading time.
            tl (numpy.array): loading time.
            nt (numpy.array): train count.
            v (numpy.array): train speed.
            L (numpy.array): train load.
        '''

        # setup
        self.distance = d
        self.unloading_time = tu
        self.loading_time = tl
        self.train_count = nt
        self.train_speed = v
        self.train_load = L

    def starting_events(self, simulator):
        ''' Add starting events to simulator calendar.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
        '''

        # add starting events
        for i in range(len(self.train_count)):
            for im in range(self.train_count[i]):
                ip = 0
                it = self.dispatch_to_terminal()
                t = simulator.time + self.distance[ip, it] / self.train_speed[im]
                data = [ip, it, im]
                simulator.add_event(t, self.on_finish_unloaded_path, data)

    def on_finish_unloaded_path(self, simulator, data):
        ''' Callback function for finishing unloaded path.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
            data (list): port, terminal and train model indexes.
        '''

        print('Loading at terminal {}'.format(data[1]))

        # add new event
        it = data[1]  # terminal index
        im = data[2]  # train model index
        t = simulator.time + self.loading_time[it, im]  # terminal loading time
        simulator.add_event(t, self.on_finish_loading, data)

    def on_finish_loading(self, simulator, data):
        ''' Callback function for finishing loading.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
            data (list): port, terminal and train model indexes.
        '''

        print('Going from terminal {} to port {}'.format(data[1], data[0]))

        # add new event
        ip = self.dispatch_to_port()  # port index
        it = data[1]  # terminal index
        im = data[2]  # train model index
        data[0] = ip
        t = simulator.time + self.distance[ip, it] / self.train_speed[im]
        simulator.add_event(t, self.on_finish_loaded_path, data)

    def on_finish_loaded_path(self, simulator, data):
        ''' Callback function for finishing loaded path.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
            data (list): port, terminal and train model indexes.
        '''

        print('Unoading at port {}'.format(data[0]))

        # add new event
        ip = data[0]  # port index
        im = data[2]  # train model index
        t = simulator.time + self.unloading_time[ip, im]  # port unloading time
        simulator.add_event(t, self.on_finish_unloading, data)

    def on_finish_unloading(self, simulator, data):
        ''' Callback function for finishing loading.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
            data (list): port, terminal and train model indexes.
        '''

        print('Going from port {} to terminal {}'.format(data[0], data[1]))

        # add new event
        it = self.dispatch_to_terminal()  # terminal index
        ip = data[0]  # port index
        im = data[2]  # train model index
        data[1] = it
        t = simulator.time + self.distance[ip, it] / self.train_speed[im]
        simulator.add_event(t, self.on_finish_unloaded_path, data)

    def dispatch_to_terminal(self):
        ''' Route train to terminal.
        '''

        return 0

    def dispatch_to_port(self):
        ''' Route train to port.
        '''

        return 0