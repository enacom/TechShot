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
        self.clear()

    def clear(self):
        ''' Clear model to start a new simulation.
        '''

        # queue
        nt = self.distance.shape[1]
        np = self.distance.shape[0]
        self.terminal_queue = [[0] for _ in range(nt)]
        self.port_queue = [[0] for _ in range(np)]

    def starting_events(self, simulator):
        ''' Add starting events to simulator calendar.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
        '''

        # add starting events
        id = 0
        for im in range(len(self.train_count)):
            for i in range(self.train_count[im]):
                ip = 0
                it = self.dispatch_to_terminal()
                t = simulator.time + self.distance[ip, it] / self.train_speed[im]
                data = [ip, it, im, id]
                simulator.add_event(t, self.on_finish_unloaded_path, data)
                id += 1

    def on_finish_unloaded_path(self, simulator, data):
        ''' Callback function for finishing unloaded path.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
            data (list): port, terminal and train model indexes.
        '''

        print('{:02.0f}:{:02.0f} Train {} arrived at terminal {}'.format(simulator.time // 3600,
                                                                         (simulator.time % 3600) // 60, data[3],
                                                                         data[1]))

        # add new event
        it = data[1]  # terminal index
        im = data[2]  # train model index
        t = max(simulator.time, self.terminal_queue[it][-1]) + self.loading_time[it, im]  # terminal loading time
        self.terminal_queue[it].append(t)
        simulator.add_event(t, self.on_finish_loading, data)

    def on_finish_loading(self, simulator, data):
        ''' Callback function for finishing loading.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
            data (list): port, terminal and train model indexes.
        '''

        print('{:02.0f}:{:02.0f} Train {} going from terminal {} to port {}'.format(simulator.time // 3600,
                                                                                    (simulator.time % 3600) // 60,
                                                                                    data[3], data[1], data[0]))

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

        print('{:02.0f}:{:02.0f} Train {} arrived at port {}'.format(simulator.time // 3600,
                                                                     (simulator.time % 3600) // 60, data[3], data[0]))

        # add new event
        ip = data[0]  # port index
        im = data[2]  # train model index
        t = max(simulator.time, self.port_queue[ip][-1]) + self.unloading_time[ip, im]  # port unloading time
        self.port_queue[ip].append(t)
        simulator.add_event(t, self.on_finish_unloading, data)

    def on_finish_unloading(self, simulator, data):
        ''' Callback function for finishing loading.

        Args:
            simulator (:obj:DES_simulator): DES simulator.
            data (list): port, terminal and train model indexes.
        '''

        print('{:02.0f}:{:02.0f} Train {} going from port {} to terminal {}'.format(simulator.time // 3600,
                                                                                    (simulator.time % 3600) // 60,
                                                                                    data[3], data[0], data[1]))

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