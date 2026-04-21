def angular_distance(self, z):
        if 'ang.diam.dist.' in self.output_bg:
            if not hasattr(self, 'output_predict'):
                self.compute()
            if type(z) == float and z in self.z_bg:
                index = self.output_interval['bg']['ang.diam.dist.'][0]+self.z_bg.index(z)
                return self.output_predict[index]
            elif len(self.z_bg) > 2:
                if 'angular_distance' not in self.cached_splines:
                    out = self.output_predict[self.output_interval['bg']['ang.diam.dist.'][0]:
                                            self.output_interval['bg']['ang.diam.dist.'][1]]
                    spline = CubicSpline(self.z_bg, out, bc_type='natural')
                    self.cached_splines['angular_distance'] = spline
                spline = self.cached_splines['angular_distance']
                if type(z) == float:
                    return float(spline(z))
                else:
                    return spline(z)
            elif self.compute_class_background:
                return super(Class, self).Hubble(z)
            else:
                raise ValueError(f"The requested redshift of {z} was not emulated and there are too few values for interpolation. You can use CLASS for all background computations by setting 'compute_class_background' to True.")
        elif self.compute_class_background:
            return super(Class, self).Hubble(z)
        else:
            raise ValueError("The angular diameter distance has not been emulated. You can use CLASS for all background computations by setting 'compute_class_background' to True.")
