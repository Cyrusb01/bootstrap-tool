import bt 

class WeighSpecified(bt.Algo):

   def __init__(self, **weights):
      super(WeighSpecified, self).__init__()
      self.weights = weights

   def __call__(self, target):
      # added copy to make sure these are not overwritten
      target.temp["weights"] = self.weights.copy()
      return True

class RebalanceAssetThreshold(bt.Algo):
    def __init__(self, threshold=0.05):
        super(RebalanceAssetThreshold, self).__init__()
        self.threshold = threshold
        self.is_initial_rebalance = True
        
        
    def __call__(self, target):
        
        if 'weights' not in target.temp:
            return True
        
        targets = target.temp['weights']
        
        if self.is_initial_rebalance:
            #print("\n", "We are in initial rebalancing.")
            
            # save value because it will change after each call to allocate. use it as base in rebalance calls
            base = target.value
            # If cash is set (it should be a value between 0-1 representing the proportion of cash to keep), 
            # calculate the new 'base'
            if 'cash' in target.temp:
                base = base * (1 - target.temp['cash'])
            for k,v in targets.items():
                target.rebalance(v, child=k, base=base, update=True)
            
            target.perm['previous_children'] = None
            target.perm["last_rebalance_date"] = target.now # Store the last rebalancing date
            
            temp_dict = {} 
            for cname in target.children:
                c = target.children[cname]
                v = c.value
                temp_dict[cname] = v
                #print(f"{cname} Initial Value: {v}")
            target.perm['previous_children'] = temp_dict
            #print(temp_dict)
            #print("Initial Portfolio Rebalance Date: ", target.now)
            #print(60*'-')
            self.is_initial_rebalance = False
            return True
        
        last_rebalance_date = target.perm["last_rebalance_date"]
        prev_children = target.perm['previous_children'] # Dict(Ticker:Value)
        
        temp_dict = {}
        # for cname in target.children:
        #     c = target.children[cname]
        #     print("Child name", c)
        #     v = c.value
        #     print("Value", v)
        #     v_prev = prev_children[cname]
        #     temp_dict[cname] = True if (v<v_prev-(v_prev*self.threshold)) or (v>v_prev+(v_prev*self.threshold)) else False

        curr_sum = 0
        for cname in target.children: #this loop gets the current value of the portfolio
            v = target.children[cname].value
            curr_sum += v
        for cname in target.children:
            v = target.children[cname].value
            if (((v/curr_sum) - targets[cname]) < -self.threshold): #this is like (.55 -.60) < -.05
                temp_dict[cname] = True
            elif (((v/curr_sum) - targets[cname]) > self.threshold): #this is like (.65 -.60) < -.05 (where .05 would be the threshold)
                temp_dict[cname] = True

        # If any Security's values deviated, then rebalance.
        if any(list(temp_dict.values())):
            #print("\n", "One of children deviated. We need to rebalance.")
            #print(temp_dict)
            curr_sum = 0
            for cname in target.children: #this loop gets the current value of the portfolio
                v = target.children[cname].value
                curr_sum += v

            for cname in target.children:
                v = target.children[cname].value
                #print((v/curr_sum)) #this is like (.55 -.60) < -.05
            
            # save value because it will change after each call to allocate. use it as base in rebalance calls
            base = target.value
            # If cash is set (it should be a value between 0-1 representing the proportion of cash to keep), 
            # calculate the new 'base'
            if 'cash' in target.temp:
                base = base * (1 - target.temp['cash'])
            for k,v in targets.items():
                target.rebalance(v, child=k, base=base, update=True)

            temp_dict = {}
            for cname in target.children:
                c = target.children[cname]
                v = c.value
                temp_dict[cname] = v
            target.perm['previous_children'] = temp_dict
            target.perm["last_rebalance_date"] = target.now
            return True
        return True

