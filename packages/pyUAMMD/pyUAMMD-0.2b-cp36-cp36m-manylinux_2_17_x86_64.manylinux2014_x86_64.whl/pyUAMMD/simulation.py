import os,sys
import uuid

import copy
import itertools

import json

import logging

class CustomFormatter(logging.Formatter):

    white = "\x1b[37;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format     = "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
    formatLine = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: white + formatLine + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + formatLine + reset,
        logging.CRITICAL: bold_red + formatLine + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,datefmt='%d/%m/%Y %H:%M:%S')
        return formatter.format(record)


class simulation:

    availModes      = ["simulationId","modelId"]

    availGroupTypes = ["Ids","notIds",
                       "Types","notTypes",
                       "ModelIds","notModelIds",
                       "SimIds","notSimIds",
                       "ModelIdsSimIds","notModelIdsSimIds"]

    id_labels = ["id",
                 "id_i","id_j","id_k","id_l"]

    id_list_labels = ["id_list","idSet_i","idSet_j","idSet_k","idSet_l"]

    def __getDataEntryLabelIndex(self,dataEntry,label):
        """
        Expected a data entry
        It returns the index of the label
        """
        for i,lbl in enumerate(dataEntry["labels"]):
            if lbl == label:
                return i
        self.log.critical(f"Required {label} but is not present.")
        sys.exit(1)

    def __getGroupsListEntriesFromComponentSet(self,componentSet):
        """
        Returns a list with all the entries which class is "Groups" and subClass "GroupsList"
        """
        groups = []
        for name,entry in componentSet.items():
            if "type" in entry:
                if entry["type"][0] == "Groups":
                    if entry["type"][1] == "GroupsList":
                        groups.append(name)

        return groups

    def __updateDataEntryIds(self,entry,idOffset):
        """
        Expected a data entry
        Data is updated if it contains id labels.
        Data is considered id if its label is in id_labels
        Data is considered id_list if its label is in id_list_labels
        """

        if "labels" not in entry.keys():
            return
        if "data" not in entry.keys():
            return

        indexToUpdate = []

        for l in entry["labels"]:
            if l in self.id_labels:
                indexToUpdate.append(self.__getDataEntryLabelIndex(entry,l))

        for d in entry["data"]:
            for i in indexToUpdate:
                d[i] += idOffset

        indexToUpdate = []

        for l in entry["labels"]:
            if l in self.id_list_labels:
                indexToUpdate.append(self.__getDataEntryLabelIndex(entry,l))

        for d in entry["data"]:
            for i in indexToUpdate:
                for n,_ in enumerate(d[i]):
                    d[i][n] += idOffset

    def __updateComponentSetIds(self,mode,componentSet,idOffset,modeOffset):
        """
        This function take a component set. It looks for all the entries that
        contains data refered to id. Then, if some id is found, it updates the
        id according to the mode and values of idOffset and modeOffset.

        Returns a copy of the component set with the updated ids.
        """

        updatedComponentSet = copy.deepcopy(componentSet)

        for dataEntry in updatedComponentSet.values():
            #If entry is not a data entry, updateDataEntryIds will do nothing
            self.__updateDataEntryIds(dataEntry,idOffset)

        return updatedComponentSet


    def __updateComponentSetGroupsLists(self,mode,componentSet,idOffset,modeOffset):
        """
        This function take a component set. It looks for all the groups list entries
        in the component set. Then, if some groups list is found, it updates the
        group definition according to the mode and values of idOffset and modeOffset.

        Returns a copy of the component set with the updated groups.
        """

        updatedComponentSet = copy.deepcopy(componentSet)

        groupsLists = self.__getGroupsListEntriesFromComponentSet(updatedComponentSet)

        #If not, doing nothing
        if len(groupsLists) == 0:
            return updatedComponentSet

        for name in groupsLists:
            self.log.debug("Updating groups list \"{}\"".format(name))

            groupDeclarations = updatedComponentSet[name]["data"]

            for groupName,groupType,selection in groupDeclarations:
                if groupType not in self.availGroupTypes:
                    self.log.error("Group type \"{}\" is not supported.".format(groupType))
                    raise Exception("Group type not supported.")
                else:
                    if groupType in ["Ids","notIds"]:
                        for n,_ in enumerate(selection):
                            selection[n] += idOffset
                    elif groupType in ["Types","notTypes"]:
                        #Do nothing
                        pass
                    elif groupType in ["ModelIds","notModelIds"]:
                        if mode == "modelId":
                            for n,_ in enumerate(selection):
                                selection[n] += modeOffset
                        else:
                            #Do nothing
                            pass
                    elif groupType in ["SimIds","notSimIds"]:
                        if mode == "simulationId":
                            for n,_ in enumerate(selection):
                                selection[n] += modeOffset
                        else:
                            #Do nothing
                            pass
                    elif groupType in ["ModelIdsSimIds","notModelIdsSimIds"]:
                        if mode == "modelId":
                            for n,_ in enumerate(selection):
                                selection[n][0] += modeOffset
                        elif mode == "simulationId":
                            for n,_ in enumerate(selection):
                                selection[n][1] += modeOffset
                        else:
                            #Do nothing
                            pass

        return updatedComponentSet

    def __appendGroups(self,mode,componentRefSet,component2AppendSet,idOffset,modeOffset):
        """
        This function takes two component set. It updates all the groupsList entries found
        in the component set to append according to the mode and values of idOffset and modeOffset.
        Then it appends the groupsList entries of the component set to append to the component set
        of reference.

        It does not return anything. Reference component set is updated.

        Rules:
        *No groups list in reference component set:
        -- No groups list in append component set -> Do nothing
        -- Groups list in append component set -> Update all components of the group list type in the set of components to be added and append them to reference
        *Groups list in reference component set:
        -- No groups list in append component set -> Do nothing
        -- Groups list in append component set ->
                1) Update all components of the group list type in the set of components to be added
                2) If the name of some group list type in the set of components to be added
                   match some name of some group list type in the reference set of components ->
                   1) If both group list types are the same -> Do nothing
                   2) If both group list types are different -> Raise an error

        """

        #Check if a entry of class "Groups" and subClass "GroupsList" is present
        groupsListsRef     = self.__getGroupsListEntriesFromComponentSet(componentRefSet)
        groupsLists2Append = self.__getGroupsListEntriesFromComponentSet(component2AppendSet)

        #If not, doing nothing
        if len(groupsListsRef) == 0:
            if len(groupsLists2Append) == 0:
                return
            else:
                updatedComponent2AppendSet = self.__updateComponentSetGroupsLists(mode,component2AppendSet,idOffset,modeOffset)
                for name in groupsLists2Append:
                    componentRefSet[name] = copy.deepcopy(updatedComponent2AppendSet[name])
        else:
            if len(groupsLists2Append) == 0:
                return
            else:
                updatedComponent2AppendSet = self.__updateComponentSetGroupsLists(mode,component2AppendSet,idOffset,modeOffset)

                for name in groupsLists2Append:
                    if name in groupsListsRef:

                        refGroupDeclarationNames      = [x[0] for x in componentRefSet[name]["data"]]
                        _2AppendGroupDeclarationNames = [x[0] for x in component2AppendSet[name]["data"]]

                        #Check there are no repeteaded names
                        if len(refGroupDeclarationNames) != len(set(refGroupDeclarationNames)):
                            self.log.error("There are repeated group declaration names in the component set of reference.")
                            raise Exception("Repeated group declaration names.")
                        if len(_2AppendGroupDeclarationNames) != len(set(_2AppendGroupDeclarationNames)):
                            self.log.error("There are repeated group declaration names in the component set to append.")
                            raise Exception("Repeated group declaration names.")

                        for gName2Append in _2AppendGroupDeclarationNames:
                            if gName2Append in refGroupDeclarationNames:
                                gRef = [gDecl for gDecl in componentRefSet[name]["data"] if gDecl[0] == gName2Append]
                                gApp = [gDecl for gDecl in updatedComponent2AppendSet[name]["data"] if gDecl[0] == gName2Append]

                                equal = not DeepDiff(gRef,gApp,ignore_order=True)
                                if equal:
                                    continue
                                else:
                                    self.log.error("Group \"{}\" already present in \"{}\".".format(gName2Append,name))
                                    raise Exception("Group already present.")
                            else:
                                g = [gDecl for gDecl in updatedComponent2AppendSet[name]["data"] if gDecl[0] == gName2Append]

                                componentRefSet[name]["data"].append(g[0])
                    else:
                        for name in groupsLists2Append:
                            componentRefSet[name] = copy.deepcopy(updatedComponent2AppendSet[name])

    def __init__(self,simulationJSON=None,debug=False):

        # Set up logger
        self.localID = uuid.uuid1().hex
        loggerName   = f"simulation:{self.localID}"

        self.log = logging.getLogger(loggerName)
        self.log.setLevel(logging.DEBUG)

        self.clog = logging.StreamHandler()
        if debug:
            self.clog.setLevel(logging.DEBUG) #<----
        else:
            self.clog.setLevel(logging.INFO) #<----

        self.clog.setFormatter(CustomFormatter())
        self.log.addHandler(self.clog)

        ########################

        if simulationJSON is not None:
            self.sim = copy.deepcopy(simulationJSON)
        else:
            self.sim = {}

        ########################

        #Checks

        stateInSim     = ("state" in self.sim)
        topologyInSim  = ("topology" in self.sim)

        if topologyInSim:
            structureInSim     = ("structure" in self.sim["topology"])

        if stateInSim and not structureInSim:
            self.log.error("Added state but not structure")
            raise ValueError("Added state but not structure")

        if stateInSim and structureInSim:
            Nsim = len(self.sim["state"]["data"])
            Nstr = len(self.sim["topology"]["structure"]["data"])

            if Nsim != Nstr:
                self.log.error("Number of particles in state and structure does not match")
                raise ValueError("Number of particles in state and structure does not match")

        ########################

        self.log.debug("Simulation created")


    def getID(self):
        return self.localID

    def getNumberOfParticles(self):
        return len(self.sim["topology"]["structure"]["data"])

    def append(self,sim2app,mode: str = "simulationId") -> None:

        from deepdiff import DeepDiff

        sim2appID = sim2app.getID()

        # Check if ID are the same
        if self.localID == sim2appID:
            self.log.error("Cannot append simulation to itself")
            raise ValueError("Cannot append simulation to itself")

        self.log.debug(f"Appending \"{sim2appID}\" to \"{self.localID}\" with mode \"{mode}\"")
        if mode not in self.availModes:
            self.log.error(f"Trying append with mode \"{mode}\", but this mode is not available. " \
                             f"Available modes are: {self.availModes}")
            raise ValueError(f"Trying append with not available mode \"{mode}\"")

        #########################
        #Appending system
        #System structure:
        #   "system": {
        #       "parameters": {"name": ..., "backup": ..., ...},
        #       "labels": [..., ...],
        #       "data": [[...],
        #                [...],
        #                ...]

        # Four cases:
        # 1) system NOT in sim and system NOT in sim2app
        # 2) system NOT in sim and system in sim2app
        # 3) system in sim and system NOT in sim2app
        # 4) system in sim and system in sim2app

        systemInSim     = ("system" in self.sim)
        systemInSim2app = ("system" in sim2app.sim)

        # 1) system NOT in sim and system NOT in sim2app
        if not systemInSim and not systemInSim2app:
            #Do nothing
            pass
        # 2) system NOT in sim and system in sim2app
        elif not systemInSim and systemInSim2app:
            self.sim["system"] = copy.deepcopy(sim2app.sim["system"])
        # 3) system in sim and system NOT in sim2app
        elif systemInSim and not systemInSim2app:
            #Do nothing
            pass
        # 4) system in sim and system in sim2app
        elif systemInSim and systemInSim2app:
            if "labels" in self.sim["system"]:
                self.log.error("Systems with labels are not supported")
                raise ValueError("Systems with labels are not supported")
            if "data" in self.sim["system"]:
                self.log.error("Systems with data are not supported")
                raise ValueError("Systems with data are not supported")

            parametersInSim     = ("parameters" in self.sim["system"])
            parametersInSim2app = ("parameters" in sim2app.sim["system"])

            if not parametersInSim and not parametersInSim2app:
                #Do nothing
                pass
            elif not parametersInSim and parametersInSim2app:
                self.sim["system"]["parameters"] = copy.deepcopy(sim2app.sim["system"]["parameters"])
            elif parametersInSim and not parametersInSim2app:
                #Do nothing
                pass
            elif parametersInSim and parametersInSim2app:

                #Check if parameter name is present in both systems.
                nameInSim     = ("name" in self.sim["system"]["parameters"])
                nameInSim2app = ("name" in sim2app.sim["system"]["parameters"])

                if not nameInSim and not nameInSim2app:
                    #Do nothing
                    pass
                elif not nameInSim and nameInSim2app:
                    self.sim["system"]["parameters"]["name"] = copy.deepcopy(sim2app.sim["system"]["parameters"]["name"])
                elif nameInSim and not nameInSim2app:
                    #Do nothing
                    pass
                elif nameInSim and nameInSim2app:
                    if mode == "modelId":
                        #Name must be the same
                        if self.sim["system"]["parameters"]["name"] != sim2app.sim["system"]["parameters"]["name"]:
                            sefl.log.error("System name must be the same. (Mode: modelId)")
                            raise ValueError("System name must be the same.")
                    elif mode == "simulationId":
                        #Combine names
                        self.sim["system"]["parameters"]["name"] = self.sim["system"]["parameters"]["name"] + \
                                                                   "_" + \
                                                                   sim2app.sim["system"]["parameters"]["name"]

                #Check if parameters share some keys. If yes, check if they are the same.
                #If parameters do not share some keys or the shared keys are the same, append them.
                for key in self.sim["system"]["parameters"]:
                    if key == "name":
                        continue
                    elif key in sim2app.sim["system"]["parameters"]:
                        if self.sim["system"]["parameters"][key] != sim2app.sim["system"]["parameters"][key]:
                            self.log.error("Shared system parameters are not the same")
                            raise ValueError("Shared system parameters are not the same")

                for key in sim2app["system"]["parameters"]:
                    if key == "name":
                        continue
                    else:
                        self.sim["system"]["parameters"][key] = sim2app["system"]["parameters"][key]


        #System appended
        #########################

        #########################
        #Appending global data
        #Global data structure:
        #   "global": {
        #       "parameters": {"temperature": ..., "box": [...,...,...], ...},
        #       "labels": ["name", "mass", "radius", "charge", ...],
        #       "data": [[...],
        #                [...],
        #                ...]

        # Four cases:
        # 1) global NOT in sim and global NOT in sim2app
        # 2) global NOT in sim and global in sim2app
        # 3) global in sim and global NOT in sim2app
        # 4) global in sim and global in sim2app

        globalInSim     = ("global" in self.sim)
        globalInSim2app = ("global" in sim2app.sim)

        # 1) global NOT in sim and global NOT in sim2app
        if not globalInSim and not globalInSim2app:
            #Do nothing
            pass
        # 2) global NOT in sim and global in sim2app
        elif not globalInSim and globalInSim2app:
            self.sim["global"] = copy.deepcopy(sim2app.sim["global"])
        # 3) global in sim and global NOT in sim2app
        elif globalInSim and not globalInSim2app:
            #Do nothing
            pass
        # 4) global in sim and global in sim2app
        elif globalInSim and globalInSim2app:

            #Process parameters

            parametersInSim     = ("parameters" in self.sim["global"])
            parametersInSim2app = ("parameters" in sim2app.sim["global"])

            if not parametersInSim and not parametersInSim2app:
                #Do nothing
                pass
            elif not parametersInSim and parametersInSim2app:
                self.sim["global"]["parameters"] = copy.deepcopy(sim2app.sim["global"]["parameters"])
            elif parametersInSim and not parametersInSim2app:
                #Do nothing
                pass
            elif parametersInSim and parametersInSim2app:

                #Check if parameters share some keys. If yes, check if they are the same.
                #If parameters do not share some keys or the shared keys are the same, append them.
                for key in self.sim["global"]["parameters"]:
                    if key in sim2app.sim["global"]["parameters"]:
                        if self.sim["global"]["parameters"][key] != sim2app.sim["global"]["parameters"][key]:
                            self.log.error("Shared global parameters are not the same")
                            raise ValueError("Shared global parameters are not the same")
                self.sim["global"]["parameters"].update(sim2app.sim["global"]["parameters"])

            #Process types
            typesInSim     = ("labels" in self.sim["global"])
            typesInSim2app = ("labels" in sim2app.sim["global"])

            if not typesInSim and not typesInSim2app:
                #Do nothing
                pass
            elif not typesInSim and typesInSim2app:
                self.sim["global"]["labels"] = copy.deepcopy(sim2app.sim["global"]["labels"])

                if "data" not in self.sim["global"]:
                    self.sim["global"]["data"] = []

                self.sim["global"]["data"].extend(copy.deepcopy(sim2app.sim["global"]["data"]))
            elif typesInSim and not typesInSim2app:
                #Do nothing
                pass
            elif typesInSim and typesInSim2app:

                #Check if global data are the same
                if self.sim["global"]["labels"] != sim2app.sim["global"]["labels"]:
                    self.log.error("Global data labels are not the same")
                    raise ValueError("Global data labels are not the same")

                #At this point labels and parameters are the same, so we can append data.
                nameIndex     = self.__getDataEntryLabelIndex(self.sim["global"],"name")
                nameIndex2app = self.__getDataEntryLabelIndex(sim2app.sim["global"],"name")

                #Iterate over data in sim2app
                for d in sim2app.sim["global"]["data"]:
                    #Check if name is already in sim. If not, append data.
                    #If name is already in sim, check if data are the same. If not, raise error.
                    if d[nameIndex2app] not in [x[nameIndex] for x in self.sim["global"]["data"]]:
                        self.sim["global"]["data"].append(d)
                    else:
                        for x in self.sim["global"]["data"]:
                            if x[nameIndex] == d[nameIndex2app]:
                                if x != d:
                                    self.log.error("Shared type name. But type data are not the same")
                                    raise ValueError("Shared type name. But type data are not the same")

        #Global data appended
        #########################


        #########################
        #Appending structure
        #Structure structure:
        #   "structure": {
        #       "labels": ["id","type","resId","chainId","modelId","simulationId"]
        #       "data": [[...],
        #                [...],
        #                ...]

        # Four cases:
        # 1) structure NOT in sim and structure NOT in sim2app
        # 2) structure NOT in sim and structure in sim2app
        # 3) structure in sim and structure NOT in sim2app
        # 4) structure in sim and structure in sim2app

        structureInSim     = ("topology" in self.sim)
        structureInSim2app = ("topology" in sim2app.sim)

        if structureInSim:
            structureInSim     = ("structure" in self.sim["topology"])
        if structureInSim2app:
            structureInSim2app = ("structure" in sim2app.sim["topology"])

        #Create offsets if reference has structure
        if structureInSim:

            #Computing id offset
            idIndex = self.__getDataEntryLabelIndex(self.sim["topology"]["structure"],"id")

            idOffset = 0
            for d in self.sim["topology"]["structure"]["data"]:
                if d[idIndex] > idOffset:
                    idOffset = d[idIndex]
            idOffset += 1

            modeOffset = 0
            if mode == "modelId":
                if "modelId" not in self.sim["topology"]["structure"]["labels"]:
                    self.sim["topology"]["structure"]["labels"].append("modelId")
                    for d in self.sim["topology"]["structure"]["data"]:
                        d.append(0)

                modeIndex = self.__getDataEntryLabelIndex(self.sim["topology"]["structure"],"modelId")
                for d in self.sim["topology"]["structure"]["data"]:
                    if d[modeIndex] > modeOffset:
                        modeOffset = d[modeIndex]
                modeOffset += 1
            elif mode == "simulationId":
                if "simulationId" not in self.sim["topology"]["structure"]["labels"]:
                    self.sim["topology"]["structure"]["labels"].append("simulationId")
                    for d in self.sim["topology"]["structure"]["data"]:
                        d.append(0)

                modeIndex = self.__getDataEntryLabelIndex(self.sim["topology"]["structure"],"simulationId")
                for d in self.sim["topology"]["structure"]["data"]:
                    if d[modeIndex] > modeOffset:
                        modeOffset = d[modeIndex]
                modeOffset += 1
            else:
                self.log.error(f"Appending mode {mode} not implemented")
                raise ValueError("Appending mode not implemented")

        # 1) structure NOT in sim and structure NOT in sim2app
        if not structureInSim and not structureInSim2app:
            #Do nothing
            pass
        # 2) structure NOT in sim and structure in sim2app
        elif not structureInSim and structureInSim2app:
            if "topology" not in self.sim:
                self.sim["topology"] = {}
            self.sim["topology"]["structure"] = copy.deepcopy(sim2app.sim["topology"]["structure"])

            idOffset   = 0
            modeOffset = 0
        # 3) structure in sim and structure NOT in sim2app
        elif structureInSim and not structureInSim2app:
            #Do nothing
            pass
        # 4) structure in sim and structure in sim2app
        elif structureInSim and structureInSim2app:

            #Handle labels
            simLabels     = self.sim["topology"]["structure"]["labels"]
            sim2appLabels = sim2app.sim["topology"]["structure"]["labels"]

            availLabels = ["id","type","resId","chainId","modelId","simulationId"]

            for label in availLabels:
                labelInSim     = (label in simLabels)
                labelInSim2app = (label in sim2appLabels)

                if not labelInSim and not labelInSim2app:
                    #Do nothing
                    pass
                elif not labelInSim and labelInSim2app:
                    self.sim["topology"]["structure"]["labels"].append(label)
                    for d in self.sim["topology"]["structure"]["data"]:
                        d.append(0)
                elif labelInSim and not labelInSim2app:
                    sim2app.sim["topology"]["structure"]["labels"].append(label)
                    for d in sim2app.sim["topology"]["structure"]["data"]:
                        d.append(0)
                elif labelInSim and labelInSim2app:
                    #Do nothing
                    pass

            #Data merging
            for structInfo in sim2app.sim["topology"]["structure"]["data"]:
                d = []
                for label in self.sim["topology"]["structure"]["labels"]:
                    if label == "id":
                        d.append(structInfo[sim2appLabels.index(label)] + idOffset)
                    elif label == mode:
                        d.append(structInfo[sim2appLabels.index(label)] + modeOffset)
                    else:
                        d.append(structInfo[sim2appLabels.index(label)])
                self.sim["topology"]["structure"]["data"].append(d)

        #Structure in sim is updated
        structureInSim = ("topology" in self.sim)
        if structureInSim:
            structureInSim = ("structure" in self.sim["topology"])

        #Structure appended
        #########################

        #########################
        #Appending state
        #State structure:
        #   "state": {
        #       "labels": ["id","position",...]
        #       "data": [[...],
        #                [...],
        #                ...]

        # Four cases:
        # 1) state NOT in sim and state NOT in sim2app
        # 2) state NOT in sim and state in sim2app
        # 3) state in sim and state NOT in sim2app
        # 4) state in sim and state in sim2app

        stateInSim     = ("state" in self.sim)
        stateInSim2app = ("state" in sim2app.sim)

        if (stateInSim or stateInSim2app) and not structureInSim:
            self.log.warning("Structure must be present in at least one simulation")
            self.log.error("Cannot merge state without any structure")
            raise ValueError("Cannot merge state without structure")

        # 1) state NOT in sim and state NOT in sim2app
        if not stateInSim and not stateInSim2app:
            #Do nothing
            pass
        # 2) state NOT in sim and state in sim2app
        elif not stateInSim and stateInSim2app:
            self.sim["state"] = copy.deepcopy(sim2app.sim["state"])
        # 3) state in sim and state NOT in sim2app
        elif stateInSim and not stateInSim2app:
            #Do nothing
            pass
        # 4) state in sim and state in sim2app
        elif stateInSim and stateInSim2app:
            #At this point, idOffset should be defined from the structure merging

            #Handle labels
            simLabels     = self.sim["state"]["labels"]
            sim2appLabels = sim2app.sim["state"]["labels"]

            availLabels = ["position","velocity","direction"]
            availLabelZeros = {"position":[0.0,0.0,0.0],
                               "velocity":[0.0,0.0,0.0],
                               "direction":[0.0,0.0,0.0,1.0]}

            if "id" not in simLabels or "id" not in sim2appLabels:
                self.log.error("Cannot merge state without id")
                raise ValueError("Cannot merge state without id")

            for label in availLabels:
                labelInSim     = (label in simLabels)
                labelInSim2app = (label in sim2appLabels)

                if not labelInSim and not labelInSim2app:
                    #Do nothing
                    pass
                elif not labelInSim and labelInSim2app:
                    self.sim["state"]["labels"].append(label)
                    for d in self.sim["state"]["data"]:
                        d.append(availLabelZeros[label])
                elif labelInSim and not labelInSim2app:
                    sim2app.sim["state"]["labels"].append(label)
                    for d in sim2app.sim["state"]["data"]:
                        d.append(availLabelZeros[label])
                elif labelInSim and labelInSim2app:
                    #Do nothing
                    pass

            #Data merging
            for stateInfo in sim2app.sim["state"]["data"]:
                d = []
                for label in self.sim["state"]["labels"]:
                    if label == "id":
                        d.append(stateInfo[sim2appLabels.index(label)] + idOffset)
                    else:
                        d.append(stateInfo[sim2appLabels.index(label)])
                self.sim["state"]["data"].append(d)

        #State appended
        #########################

        #########################
        #Appending integrator
        #Integrator structure:
        #   "integrator": {
        #       "groups": {...} #Groups list, optional
        #       "integrator1": {
        #           "type": ["Class1","SubClass1"],
        #           "parameters": {
        #               "param1": "value1",
        #               "param2": "value2",
        #               ...
        #           }
        #       },
        #       "integrator2": {
        #           "type": ["Class2","SubClass2"],
        #           "parameters": {
        #               "param1": "value1",
        #               "param2": "value2",
        #               ...
        #           }
        #       },
        #       ...,
        #       "schedule": {
        #           "type": ["Schedule","Integrator"],
        #           "labels": ["order","integrator","step"],
        #           "data": [[...,...,...],
        #                    [...,...,...],
        #                    ...]
        #       }
        #   }

        # Four cases:
        # 1) integrator NOT in sim and integrator NOT in sim2app
        # 2) integrator NOT in sim and integrator in sim2app
        # 3) integrator in sim and integrator NOT in sim2app
        # 4) integrator in sim and integrator in sim2app

        integratorInSim     = ("integrator" in self.sim)
        integratorInSim2app = ("integrator" in sim2app.sim)

        if (integratorInSim or integratorInSim2app) and not structureInSim:
            self.log.warning("Structure must be present in at least one simulation")
            self.log.error("Cannot merge integrator without any structure")
            raise ValueError("Cannot merge integrator without structure")

        # 1) integrator NOT in sim and integrator NOT in sim2app
        if not integratorInSim and not integratorInSim2app:
            #Do nothing
            pass
        # 2) integrator NOT in sim and integrator in sim2app
        elif not integratorInSim and integratorInSim2app:
            #In this case the only thing to do is update the sim2app["integrator"] groups list entries (if any)
            self.sim["integrator"] = self.__updateComponentSetGroupsLists(mode,sim2app["integrator"],idOffset,modeOffset)
        # 3) integrator in sim and integrator NOT in sim2app
        elif integratorInSim and not integratorInSim2app:
            #Do nothing
            pass
        # 4) integrator in sim and integrator in sim2app
        elif integratorInSim and integratorInSim2app:
            #We append (after updating) the groupsLists in sim2app["integrator"] to sim["integrator"]
            self.__appendGroups(mode,self.sim["integrator"],sim2app["integrator"],idOffset,modeOffset)

            integratorsSim     = [k for k in self.sim["integrator"].keys() if "Schedule" not in self.sim["integrator"][k]["type"]]
            integratorsSim2app = [k for k in sim2app.sim["integrator"].keys() if "Schedule" not in sim2app.sim["integrator"][k]["type"]]

            for inte2app in integratorsSim2app:
                if inte2app not in integratorsSim:
                    self.sim["integrator"][inte2app] = copy.deepcopy(sim2app["integrator"][inte2app])
                else:
                    #If are equal do nothing. Else raise error
                    equal = not DeepDiff(self.sim["integrator"][inte2app],
                                         sim2app["integrator"][inte2app],
                                         ignore_order=True,report_repetition=True)
                    if not equal:
                        self.log.error("Cannot merge integrator with different parameters")
                        raise ValueError("Cannot merge integrator with different parameters")

            #Merge schedule
            scheduleName = [k for k in self.sim["integrator"].keys() if "Schedule" in self.sim["integrator"][k]["type"]]
            if len(scheduleName) == 0:
                self.log.error("Cannot merge integrator without schedule")
                raise ValueError("Cannot merge integrator without schedule")
            elif len(scheduleName) > 1:
                self.log.error("Cannot merge integrator with more than one schedule")
                raise ValueError("Cannot merge integrator with more than one schedule")

            scheduleName = scheduleName[0]

            scheduleOffset = 0
            for inte in self.sim["integrator"][scheduleName]["data"]:
                if inte[0] > scheduleOffset: #it assumes that the schedule is ordered and well formed
                    scheduleOffset = inte[0]

            scheduleName2app = [k for k in sim2app.sim["integrator"].keys() if "Schedule" in sim2app.sim["integrator"][k]["type"]]
            if len(scheduleName2app) == 0:
                self.log.error("Cannot merge integrator without schedule")
                raise ValueError("Cannot merge integrator without schedule")
            elif len(scheduleName2app) > 1:
                self.log.error("Cannot merge integrator with more than one schedule")
                raise ValueError("Cannot merge integrator with more than one schedule")

            scheduleName2app = scheduleName2app[0]

            for inte in sim2app.sim["integrator"][scheduleName2app]["data"]:
                inteName = inte[1]
                if inteName not in integratorsSim:
                    inte[0] += scheduleOffset
                    self.sim["integrator"][scheduleName]["data"].append(inte)

        #Integrator appended
        #########################

        #########################
        #Appending simulation step
        #Simulation steps structure:
        #   "simulationStep": {
        #       "groups": {...} #Groups list, optional
        #       "step1": {
        #           "type": ["Class1","SubClass1"],
        #           "parameters": {
        #               "intervalStep": "value",
        #               "startStep": "value", #optional
        #               "endStep": "value", #optional
        #               "param2": "value2",
        #               ...
        #           }
        #           "labels": ["label1","label2",...],
        #           "data": [[...],
        #                    [...],
        #                    ...]
        #       },
        #       "step2": {
        #           "type": ["Class2","SubClass2"],
        #           "parameters": {
        #               "intervalStep": "value",
        #               "startStep": "value", #optional
        #               "endStep": "value", #optional
        #               "param2": "value2",
        #               ...
        #           }
        #           "labels": ["label1","label2",...],
        #           "data": [[...],
        #                    [...],
        #                    ...]
        #       },
        #       ...,
        #   }

        # Four cases:
        # 1) simulationStep NOT in sim and simulationStep NOT in sim2app
        # 2) simulationStep NOT in sim and simulationStep in sim2app
        # 3) simulationStep in sim and simulationStep NOT in sim2app
        # 4) simulationStep in sim and simulationStep in sim2app

        simulationStepInSim     = ("simulationStep" in self.sim)
        simulationStepInSim2app = ("simulationStep" in sim2app.sim)

        if (simulationStepInSim or simulationStepInSim2app) and not structureInSim:
            self.log.warning("Structure must be present in at least one simulation")
            self.log.error("Cannot merge simulationStep without any structure")
            raise ValueError("Cannot merge simulationStep without structure")

        # 1) simulationStep NOT in sim and simulationStep NOT in sim2app
        if not simulationStepInSim and not simulationStepInSim2app:
            #Do nothing
            pass
        # 2) simulationStep NOT in sim and simulationStep in sim2app
        elif not simulationStepInSim and simulationStepInSim2app:
            #Check if the sim2app have particles defined.
            if structureInSim2app:
                #In this case, we first update the groups in sim2app and then de ids in the remainder entries
                self.sim["simulationStep"] = self.__updateComponentSetIds(mode,
                                                                          self.__updateComponentSetGroupsLists(mode,
                                                                                                               sim2app["simulationStep"],
                                                                                                               idOffset,modeOffset),
                                                                          idOffset,modeOffset)
            else:
                self.sim["simulationStep"] = copy.deepcopy(sim2app["simulationStep"])

        # 3) simulationStep in sim and simulationStep NOT in sim2app
        elif simulationStepInSim and not simulationStepInSim2app:
            #Do nothing
            pass
        # 4) simulationStep in sim and simulationStep in sim2app
        elif simulationStepInSim and simulationStepInSim2app:

            #Check if the sim2app have particles defined.
            if structureInSim2app:
                #We append (after updating) the groupsLists in sim2app["simulationStep"] to sim["simulationStep"]
                updatedSimulationStep2app =  self.__updateComponentSetIds(mode,sim2app["simulationStep"],idOffset,modeOffset)
                self.__appendGroups(mode,self.sim["simulationStep"],updatedSimulationStep2app,idOffset,modeOffset)
            else:
                updatedSimulationStep2app = copy.deepcopy(sim2app["simulationStep"])
                self.__appendGroups(mode,self.sim["simulationStep"],updatedSimulationStep2app,0,0)

            simulationStepsSim     = [k for k in self.sim["simulationStep"].keys() if self.sim["simulationStep"][k]["type"] != ["Groups","GroupsList"]]
            simulationStepsSim2app = [k for k in sim2app.sim["simulationStep"].keys() if sim2app["simulationStep"][k]["type"] != ["Groups","GroupsList"]]

            for simStep2app in simulationStepsSim2app:
                if simStep2app not in simulationStepsSim:
                    self.sim["simulationStep"][simStep2app] = copy.deepcopy(updatedSimulationStep2app[simStep2app])
                else:
                    equalParam = not DeepDiff(self.sim["simulationStep"][simStep2app],
                                              updatedSimulationStep2app[simStep2app],
                                              ignore_order=True,report_repetition=True,
                                              exclude_paths=["root['data']"]) #Note data is excluded from comparison
                    if equalParam:

                        if "data" not in self.sim["simulationStep"][simStep2app] and "data" not in updatedSimulationStep2app[simStep2app]:
                            continue

                        dataSim     = self.sim["simulationStep"][simStep2app]["data"]
                        dataSim2app = updatedSimulationStep2app[simStep2app]["data"]

                        if len(dataSim) != len(dataSim2app):
                            equalData = False
                        else:
                            equalData = not DeepDiff(dataSim,dataSim2app,ignore_order=True,report_repetition=True)

                        if equalData:
                            pass
                        else:
                            self.sim["simulationStep"][simStep2app]["data"].extend(updatedSimulationStep2app[simStep2app]["data"])

                    else:
                        self.log.error("Cannot merge simulationStep with different parameters")
                        raise ValueError("Cannot merge simulationStep with different parameters")

        #Simulation step appended
        #########################

        #########################
        #Appending force field
        #Force field structure:
        #   "forceField": {
        #       "groups": {...} #Groups list, optional
        #       "interaction1": {
        #           "type": ["Class1","SubClass1"],
        #           "parameters": {
        #               "param1": "value",
        #               "param2": "value2",
        #               ...
        #           }
        #           "labels": ["label1","label2",...],
        #           "data": [[...],
        #                    [...],
        #                    ...]
        #       },
        #       "interaction2": {
        #           "type": ["Class2","SubClass2"],
        #           "parameters": {
        #               "param1": "value",
        #               "param2": "value2",
        #               ...
        #           }
        #           "labels": ["label1","label2",...],
        #           "data": [[...],
        #                    [...],
        #                    ...]
        #       },
        #       ...,
        #   }

        # Four cases:
        # 1) forceField NOT in sim and forceField NOT in sim2app
        # 2) forceField NOT in sim and forceField in sim2app
        # 3) forceField in sim and forceField NOT in sim2app
        # 4) forceField in sim and forceField in sim2app

        forceFieldInSim     = ("topology" in self.sim)
        forceFieldInSim2app = ("topology" in sim2app.sim)

        if forceFieldInSim:
            forceFieldInSim     = ("forceField" in self.sim["topology"])
        if forceFieldInSim2app:
            forceFieldInSim2app = ("forceField" in sim2app.sim["topology"])

        if (forceFieldInSim or forceFieldInSim2app) and not structureInSim:
            self.log.warning("Structure must be present in at least one simulation")
            self.log.error("Cannot merge forceField without any structure")
            raise ValueError("Cannot merge forceField without structure")

        # 1) forceField NOT in sim and forceField NOT in sim2app
        if not forceFieldInSim and not forceFieldInSim2app:
            #Do nothing
            pass
        # 2) forceField NOT in sim and forceField in sim2app
        elif not forceFieldInSim and forceFieldInSim2app:
            #Check if the sim2app have particles defined.
            if structureInSim2app:
                #In this case, we first update the groups in sim2app and then de ids in the remainder entries
                self.sim["topology"]["forceField"] = self.__updateComponentSetIds(mode,
                                                                                  self.__updateComponentSetGroupsLists(mode,
                                                                                                                       sim2app["topology"]["forceField"],
                                                                                                                       idOffset,modeOffset),
                                                                                  idOffset,modeOffset)
            else:
                self.sim["topology"]["forceField"] = copy.deepcopy(sim2app["topology"]["forceField"])

        # 3) forceField in sim and forceField NOT in sim2app
        elif forceFieldInSim and not forceFieldInSim2app:
            #Do nothing
            pass
        # 4) forceField in sim and forceField in sim2app
        elif forceFieldInSim and forceFieldInSim2app:

            #Check if the sim2app have particles defined.
            if structureInSim2app:
                #We append (after updating) the groupsLists in sim2app["forceField"] to sim["forceField"]
                updatedForceField2app =  self.__updateComponentSetIds(mode,sim2app["topology"]["forceField"],idOffset,modeOffset)
                self.__appendGroups(mode,self.sim["topology"]["forceField"],updatedForceField2app,idOffset,modeOffset)
            else:
                updatedForceField2app = copy.deepcopy(sim2app["topology"]["forceField"])
                self.__appendGroups(mode,self.sim["topology"]["forceField"],updatedForceField2app,0,0)

            forceFieldSim     = [k for k in self.sim["topology"]["forceField"].keys() if self.sim["topology"]["forceField"][k]["type"] != ["Groups","GroupsList"]]
            forceFieldSim2app = [k for k in sim2app.sim["topology"]["forceField"].keys() if sim2app["topology"]["forceField"][k]["type"] != ["Groups","GroupsList"]]

            for ff2app in forceFieldSim2app:
                if ff2app not in forceFieldSim:
                    self.sim["topology"]["forceField"][ff2app] = copy.deepcopy(updatedForceField2app[ff2app])
                else:
                    equalParam = not DeepDiff(self.sim["topology"]["forceField"][ff2app],
                                              updatedForceField2app[ff2app],
                                              ignore_order=True,report_repetition=True,
                                              exclude_paths=["root['data']"]) #Note data is excluded from comparison
                    if equalParam:

                        if "data" not in self.sim["topology"]["forceField"][ff2app] or "data" not in updatedForceField2app[ff2app]:
                            continue

                        dataSim     = self.sim["topology"]["forceField"][ff2app]["data"]
                        dataSim2app = updatedForceField2app[ff2app]["data"]

                        if len(dataSim) != len(dataSim2app):
                            equalData = False
                        else:
                            equalData = not DeepDiff(dataSim,dataSim2app,ignore_order=True,report_repetition=True)

                        if equalData:
                            pass
                        else:
                            self.sim["topology"]["forceField"][ff2app]["data"].extend(updatedForceField2app[ff2app]["data"])

                    else:
                        self.log.error("Cannot merge forceField with different parameters")
                        raise ValueError("Cannot merge forceField with different parameters")

        #Force field appended
        #########################

    def write(self,output:str):
        self.log.debug("Writting to json...")

        try:
            import writeJSON
            self.log.debug("Writting with writeJSON")
            writeJSON.writeJSON(self.sim,output)
        except:
            import jsbeautifier
            self.log.warning("Writting with legacy")
            with open(output,"w") as f:
                opts = jsbeautifier.default_options()
                opts.indent_size  = 2
                f.write(jsbeautifier.beautify(json.dumps(self.sim), opts))

    def setValue(self,path,value):
        simTmp = self.sim
        for p in path[:-1]:
            simTmp = simTmp[p]
        simTmp[path[-1]] = value

    #With the following methods simulation behaves like a dict

    def __getitem__(self,key):
        return self.sim[key]

    def __setitem__(self,key,value):
        self.sim[key]=value

    def __delitem__(self, key):
        del self.sim[key]

    def __contains__(self, key):
        return key in self.sim

    def keys(self):
        return list(self.sim.keys())

    def values(self):
        return list(self.sim.values())

    def items(self):
        return list(self.sim.items())

    def pop(self, key, default=None):
        try:
            value = self.sim[key]
            del self.sim[key]
            return value
        except KeyError:
            if default is not None:
                return default
            else:
                raise

    def run(self):
        self.log.debug("Runing simulation...")

        try:
            import UAMMDlauncher
            UAMMDlauncher.UAMMDlauncher(self.sim)
        except:
            self.log.error("Something went wrong with UAMMDlauncher")
