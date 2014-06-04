from django import forms
from django.utils.translation import gettext as _

class RoundForms(forms.Form):
    ERAS = (
        (0, _('Ancient')),
        (1, _('Medieval')),
        (2, _('Gunpowder/Industrial')),
        (3, _('Modern')),
    )
    
    era = forms.ChoiceField(choices=ERAS, label=_('Era'), initial=0, help_text='', widget=forms.Select(attrs={'placeholder': _('Era'), 'class': 'form-control', 'required' : True}))
    die_roll_result = forms.IntegerField(min_value=2, max_value=12, label=_('Die Roll Result'), initial=2, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Die Roll Result'), 'class': 'form-control', 'required' : True}))
    
    village = forms.IntegerField(min_value=0, label=_('Simple'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Simple'), 'class': 'form-control', 'required' : True}))
    fertile_village = forms.IntegerField(min_value=0, label=_('Fertile'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Fertile'), 'class': 'form-control', 'required' : True}))

    town = forms.IntegerField(min_value=0, label=_('Simple'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Simple'), 'class': 'form-control', 'required' : True}))
    fertile_town = forms.IntegerField(min_value=0, label=_('Fertile'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Fertile'), 'class': 'form-control', 'required' : True}))

    city = forms.IntegerField(min_value=0, label=_('Simple'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Simple'), 'class': 'form-control', 'required' : True}))
    fertile_city = forms.IntegerField(min_value=0, label=_('Fertile'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Fertile'), 'class': 'form-control', 'required' : True}))

    metropolis = forms.IntegerField(min_value=0, label=_('Simple'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Simple'), 'class': 'form-control', 'required' : True}))
    fertile_metropolis = forms.IntegerField(min_value=0, label=_('Fertile'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Fertile'), 'class': 'form-control', 'required' : True}))
    
    wine = forms.IntegerField(min_value=0, label=_('Wine'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Wine'), 'class': 'form-control', 'required' : True}))
    horses = forms.IntegerField(min_value=0, label=_('Horses'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Horses'), 'class': 'form-control', 'required' : True}))
    iron = forms.IntegerField(min_value=0, label=_('Iron'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Iron'), 'class': 'form-control', 'required' : True}))
    gems = forms.IntegerField(min_value=0, label=_('Gems'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Gems'), 'class': 'form-control', 'required' : True}))
    spices = forms.IntegerField(min_value=0, label=_('Spices'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Spices'), 'class': 'form-control', 'required' : True}))
    oil = forms.IntegerField(min_value=0, label=_('Oil'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Oil'), 'class': 'form-control', 'required' : True}))
    coal = forms.IntegerField(min_value=0, label=_('Coal'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Coal'), 'class': 'form-control', 'required' : True}))
    rare_metals = forms.IntegerField(min_value=0, label=_('Rare metals'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Rare metals'), 'class': 'form-control', 'required' : True}))
    
    technology = forms.IntegerField(min_value=0, label=_('Technology'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Technology'), 'class': 'form-control', 'required' : True}))
    
    wonders_of_world = forms.IntegerField(min_value=0, label=_('Wonders of the world'), initial=0, help_text='', widget=forms.NumberInput(attrs={'placeholder': _('Wonders of the world'), 'class': 'form-control', 'required' : True}))

    def clean_era(self):
        return int(self.cleaned_data.get('era', 0))
    
    def _calculate_monopoly(self, number, monopoly_1, monopoly_2, monopoly_3):
        if number == 3:
            monopoly_1 += 1
        elif number == 4:
            monopoly_2 += 1
        elif number == 5:
            monopoly_3 += 1
            
        return monopoly_1, monopoly_2, monopoly_3
        
    def calculate(self):
        result = dict(city=0, critical_resource=False, unique_resources=0, monopoly_1=0, monopoly_2=0, monopoly_3=0, total=0)
        
        # City gold calculate
        result.update(city=(
            self.cleaned_data.get('village', 0)
            + self.cleaned_data.get('fertile_village', 0)*2
            + self.cleaned_data.get('town', 0)*2
            + self.cleaned_data.get('fertile_town', 0)*3
            + self.cleaned_data.get('city', 0)*3
            + self.cleaned_data.get('fertile_city', 0)*4
            + self.cleaned_data.get('metropolis', 0)*4
            + self.cleaned_data.get('fertile_metropolis', 0)*5
        ))
        
        # Find critical resource
        table_critical_resource = {
            0: {i+1: 'wine' if i < 3 else 'horses' if i < 5 else 'iron' if i < 8 else 'gems' if i < 10 else 'spices' for i in range(12)},
            1: {i+1: 'wine' if i < 3 else 'gems' if i < 5 else 'spices' if i < 8 else 'iron' if i < 10 else 'horses' for i in range(12)},
            2: {i+1: 'oil' if i < 3 else 'gems' if i < 5 else 'coal' if i < 8 else 'iron' if i < 10 else 'horses' for i in range(12)},
            3: {i+1: 'coal' if i < 3 else 'rare_metals' if i < 5 else 'oil' if i < 8 else 'oil' if i < 10 else 'iron' for i in range(12)},
        }
        
        die_roll_result = self.cleaned_data.get('die_roll_result', 0)
        era = self.cleaned_data.get('era', 0)
        print(die_roll_result, era)
        if die_roll_result > 0:
            result.update(critical_resource=(self.cleaned_data.get(table_critical_resource[era][die_roll_result], 0) > 0))
            
        # Unique resources
        wine = self.cleaned_data.get('wine', 0)
        horses = self.cleaned_data.get('horses', 0)
        iron = self.cleaned_data.get('iron', 0)
        gems = self.cleaned_data.get('gems', 0)
        spices = self.cleaned_data.get('spices', 0)
        oil = self.cleaned_data.get('oil', 0)
        coal = self.cleaned_data.get('coal', 0)
        rare_metals = self.cleaned_data.get('rare_metals', 0)
        
        result.update(unique_resources = (
            (1 if wine > 0 else 0)
            + (1 if horses > 0 else 0)
            + (1 if iron > 0 else 0)
            + (1 if gems > 0 else 0)
            + (1 if spices > 0 else 0)
            + (1 if oil > 0 else 0)
            + (1 if coal > 0 else 0)
            + (1 if rare_metals > 0 else 0)
        ))
        
        # Monopoly
        monopoly_1 = monopoly_2 = monopoly_3 = 0
        monopoly_1, monopoly_2, monopoly_3 = self._calculate_monopoly(wine, monopoly_1, monopoly_2, monopoly_3)
        monopoly_1, monopoly_2, monopoly_3 = self._calculate_monopoly(horses, monopoly_1, monopoly_2, monopoly_3)
        monopoly_1, monopoly_2, monopoly_3 = self._calculate_monopoly(iron, monopoly_1, monopoly_2, monopoly_3)
        monopoly_1, monopoly_2, monopoly_3 = self._calculate_monopoly(gems, monopoly_1, monopoly_2, monopoly_3)
        monopoly_1, monopoly_2, monopoly_3 = self._calculate_monopoly(spices, monopoly_1, monopoly_2, monopoly_3)
        monopoly_1, monopoly_2, monopoly_3 = self._calculate_monopoly(oil, monopoly_1, monopoly_2, monopoly_3)
        monopoly_1, monopoly_2, monopoly_3 = self._calculate_monopoly(coal, monopoly_1, monopoly_2, monopoly_3)
        monopoly_1, monopoly_2, monopoly_3 = self._calculate_monopoly(rare_metals, monopoly_1, monopoly_2, monopoly_3)
        
        result.update(monopoly_1=monopoly_1, monopoly_2=monopoly_2, monopoly_3=monopoly_3)
        
        # Calculate total
        total = (
            result['city']
            + result['city'] if result['critical_resource'] else 0
            + result['unique_resources']*self.cleaned_data.get('technology', 0)
            + result['monopoly_1']*20
            + result['monopoly_2']*40
            + result['monopoly_3']*80
        )
        
        result.update(total=max(total, 10))
        
        result.update(settlement_size=(self.cleaned_data.get('village', 0)
            + self.cleaned_data.get('fertile_village', 0)
            + self.cleaned_data.get('town', 0)*2
            + self.cleaned_data.get('fertile_town', 0)*2
            + self.cleaned_data.get('city', 0)*3
            + self.cleaned_data.get('fertile_city', 0)*3
            + self.cleaned_data.get('metropolis', 0)*4
            + self.cleaned_data.get('fertile_metropolis', 0)*4
        ))
        
        result.update(technologies=self.cleaned_data.get('technology', 0)*2)
        result.update(wonders_of_world=self.cleaned_data.get('wonders_of_world', 0)*3)
        
        result.update(victory_points=result['settlement_size'] + result['technologies'] + result['wonders_of_world'])

        return result