from syned.beamline.optical_element_with_surface_shape import OpticalElementsWithMultipleShapes
from syned.beamline.shape import Plane

class Lens(OpticalElementsWithMultipleShapes):
    def __init__(self,
                 name="Undefined",
                 surface_shape1=None,
                 surface_shape2=None,
                 boundary_shape=None,
                 material="",
                 thickness=0.0):

        if surface_shape1 is None: surface_shape1 = Plane()
        if surface_shape2 is None: surface_shape2 = Plane()

        super(Lens, self).__init__(name=name,
                                   boundary_shape=boundary_shape,
                                   surface_shapes=[surface_shape1, surface_shape2])
        self._material = material
        self._thickness = thickness

        # support text contaning name of variable, help text and unit. Will be stored in self._support_dictionary
        self._set_support_text([
                    ("name",                "Name" ,                                "" ),
                    ("surface_shape1",      "Surface shape 1",                      "" ),
                    ("surface_shape2",      "Surface shape 2",                      ""),
                    ("boundary_shape",      "Boundary shape",                       "" ),
                    ("material",            "Material (element, compound or name)", "" ),
                    ("thickness",           "Thickness",                            "m"),
            ] )

    def get_thickness(self):
        return self._thickness

    def get_material(self):
        return self._material

    def get_boundary_shape(self):
        return self._boundary_shape

    def get_surface_shape1(self):
        return self.get_surface_shape(index=0)

    def get_surface_shape2(self):
        return self.get_surface_shape(index=1)

