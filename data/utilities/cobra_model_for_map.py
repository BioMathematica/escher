import cobra.io, re, json, os
from IPython.display import HTML

m = cobra.io.load_matlab_model('../models/iJO1366.mat')
directory = "../maps"
version = 'v0.4.0'

if version=='v0.1.0':
    # Version 0.1 model
    data = []
    for reaction in m.reactions:
        mets = []
        for metabolite_id, coefficient in reaction._metabolites.iteritems():
            mets.append({'cobra_id': unicode(metabolite_id),
                         'coefficient': coefficient})
        data.append({'cobra_id': unicode(reaction.id),
                     'metabolites': mets})

    out_file = os.path.join(directory, 'cobra_model_0.1.json')
    with open(out_file, 'w') as f:
        json.dump(data, f)
elif version=='v0.2.0':
    # Version 0.2 model
    reactions = {}
    for reaction in m.reactions:
        mets = {}
        for metabolite_id, coefficient in reaction._metabolites.iteritems():
            mets[unicode(metabolite_id)] = {'coefficient': coefficient}
        reactions[unicode(reaction.id)] = {'metabolites': mets}
    data = {'reactions': reactions}

    out_file = os.path.join(directory, 'cobra_model_0.2.json')
    with open(out_file, 'w') as f:
        json.dump(data, f)
        
elif version=='v0.4.0':
    # Version 0.4 model
    reactions = {}
    compartments = {'_c': 'cytosol', '_p': 'periplasm', '_e': 'extracellular'}
    for reaction in m.reactions:
        mets = {}
        for metabolite, coefficient in reaction._metabolites.iteritems():
            # replace __ with -
            the_id = unicode(metabolite.id).replace('__', '-')
            
            # get the compartment
            try:
                compartment = compartments[metabolite.id[-2:]]
                bigg_id_no_compartment = the_id[:-2]
            except KeyError:
                raise Exception('Compartment not found for: %s' % metabolite.id)

            # add metabolite
            mets[the_id] = { 'coefficient': coefficient,
                             'compartment': compartment,
                             'name': metabolite.name,
                             'bigg_id': bigg_id_no_compartment,
                             'bigg_id_compartmentalized': the_id,
                             'formula': unicode(metabolite.formula) }
            
        # replace __ with -
        the_id = unicode(reaction.id).replace('__', '-')

        # save reaction
        reactions[the_id] = { 'metabolites': mets,
                              'reversibility': reaction.reversibility,
                              'name': reaction.name }

    data = {'reactions': reactions}

    out_file = os.path.join(directory, 'iJO1366_visbio_model_0.4.0.json')
    with open(out_file, 'w') as f:
        json.dump(data, f)
