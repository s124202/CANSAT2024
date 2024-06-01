def measure_index(
        self, temperature: float = 25, relative_humidity: float = 50
    ) -> int:
        
        raw = self.measure_raw(temperature, relative_humidity)
        if raw < 0:
            return -1