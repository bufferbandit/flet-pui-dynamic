from PUI.flet import FBase
import typing
import flet



def typehint_hierarchy_contains_typehint(target_type, type_to_check):
    if hasattr(target_type, "__origin__") and target_type.__origin__ is not None:
        args = typing.get_args(target_type)
        if any(arg == type_to_check for arg in args):
            return True
        # Recursively check if any arguments are containers with their own arguments
        return any(typehint_hierarchy_contains_typehint(arg, type_to_check)
                   for arg in args if hasattr(arg, "__origin__"))
    return False



class Root(FBase):

    def __init__(self):
        super().__init__()

    def addChild(self, idx, child):
        if idx == 0:
            self.inner.add(child.outer)

    def removeChild(self, idx, child):
        if idx == 0:
            self.inner.remove(child.outer)



class DynamicPuiFletControl(FBase):
    element_custom_control_data = None
    def __init__(self, *args,requested_attribute=None,custom_control_data=None,**kwargs):
        super().__init__()
        self.requested_attribute = requested_attribute
        self.custom_control_data = custom_control_data
        self.args = args
        self.kwargs = kwargs


    def update(self, prev):
        self.inner_element = getattr(flet, self.requested_attribute)

        self.element_custom_control_data = self.custom_control_data.get(
            f"{self.inner_element.__module__}.{self.inner_element.__name__}")
        self.ui = self.inner_element(*self.args, **self.kwargs)

        if prev and prev.ui:
            # The setting of this makes the child-holding work.
            # I'm not exactly sure why this works and in the future
            # this should be investigated and properly fixed if necessary,
            if (self.element_custom_control_data
                    and self.element_custom_control_data.get("parent") is True):
                self.ui = prev.ui
            self.ui._Control__uid = prev.ui._Control__uid
            self.ui._Control__page = prev.ui._Control__page
            self.ui.update()
        super().update(prev)




    def check_child_holder_for_control_sequence(self, childholding_attr_name):


        child_holder_element_type = typing.get_type_hints(
            # Normally I'd probably use this on the getter but strangely enough
            # that doesn't seem to work for all classes so doing it on the setter instead
            getattr(self.ui.__class__, childholding_attr_name).fset
        ).get("value")

        # Now check if somewhere in the typehint hierarchy it contains a sequence of controls
        is_sequence_of_controls = typehint_hierarchy_contains_typehint(child_holder_element_type, typing.Sequence[flet.Control])

        return is_sequence_of_controls

    def addChild(self, idx, child):

        childholding_attr_name = self.element_custom_control_data.get("childholder") or "controls"
        child_holder_element = getattr(self.ui, childholding_attr_name)

        is_sequence_of_controls = self.check_child_holder_for_control_sequence(childholding_attr_name)

        # If the child is a sequence of controls, insert it in there
        if is_sequence_of_controls:

            self.ui.controls.insert(idx, child.outer)
            # child_holder_element.insert(idx, child.outer)

        # Otherwise set the child attribute to it
        else:

            # self.ui.clean()
            setattr(self.ui, childholding_attr_name, child.outer)

        self.ui.update()

    def removeChild(self, idx, child):
        # print("remove childs ",self.ui.controls)
        # self.ui.controls.pop(idx)
        # self.ui.update()

        childholding_attr_name = "controls"  # ( self.element_custom_control_data.get("childholder") or "controls")
        child_holder_element = getattr(self.ui, childholding_attr_name)

        is_sequence_of_controls = self.check_child_holder_for_control_sequence(childholding_attr_name)

        # If the child is a sequence of controls, insert it in there
        if is_sequence_of_controls:
            # self.ui.controls.insert(idx, child.outer)
            #child_holder_element.insert(idx, child.outer)
            if  self.ui.controls:
                self.ui.controls.pop(idx)
            # else:
            #     raise Exception("Trying to pop from empty children")

        # Otherwise set the child attribute to it
        else:
            # self.ui.clean()
            setattr(self.ui, childholding_attr_name, None)

        self.ui.update()




class DynamicFletFactory:

    custom_control_data = {
        "flet_core.container.Container": {
            "parent": True,
            "childholder":"content",
        },
        "flet_core.column.Column": {
            "parent": True
        },
        "flet_core.row.Row": {
            "parent": True
        },
    }


    def __init__(self, custom_control_data=None):
        if custom_control_data is not None:
            self.custom_control_data = custom_control_data


    def __getattr__(self, key):
        self.requested_attribute=key
        return self

    def __call__(self, *args, **kwargs):


        # This is a bizarre workaround and I cannot figure out how to work without it.
        # This creates exactly the same objects, but when I'd just call one it will
        # result in it giving errors in the PUI conditional logic
        d = {k: type(f"dff.{k}", (DynamicPuiFletControl,), {}) for k in dir(flet)}
        dynamic_pui_flet_control = (d.get(self.requested_attribute)
                                    # When dynamic_pui_flet_control is None, it indicates
                                    # that it does not exist. Continuing from this point
                                    # does not make sense, as it cannot be looked up in the
                                    # dictionary and thus won't return a callable method.
                                    # Even if it could be looked up, it would lead to an
                                    # exception down the line when trying to access a non-existent
                                    # attribute on flet. To avoid this situation, we intentionally
                                    # raise an AttributeError here, providing a more informative stack trace.
                                    or (lambda *_,**__:getattr(flet, self.requested_attribute)))
        return dynamic_pui_flet_control(*args, requested_attribute=self.requested_attribute,custom_control_data=self.custom_control_data, **kwargs)




dff = DynamicFletFactory()




# A little trick to trick the linter into thinking dft is flet.
# useful because it will provide the dft object with the autocompletion
# of regular flet
if None: dff = flet