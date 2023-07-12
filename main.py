# This is project to answer the question why there is only left handed protein exist in the world.


# Background: when we are trying to synthesis some amino acid in the lab, the probability of appearing amino acid for left-
# and right handed is equal, and all of their physical and chemical character is the same, thus we can't distinguish them from
# each other. But in the real world, there is only left-handed amino acid, in the model, we want to verify the probability that
# there is only one kind of amino acid can exist even if there are two chirality exist.

# method: we use computer to simulate there are two kinds of species, and they are not compatible with each other, the
# limitation of the environment is 10000, and those two species will die, their age is around 50 cycles + random .
# those species will replicate themselves. if their number reach to the environment limitation, the replication will stop.

# assumption: left handed amino acid and right handed amino acid can't exist in the same animals.

import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st



class LeftHanded():
    def __init__(self):
        # this is the attribute of the aminoacid
        self.age = 0

    def replicate(self):
        # this function sever for replication
        return LeftHanded()

    def grow(self):
        # the age will plus one after each cycle, and will dye when it reach it's life span
        self.age += 1


class RightHanded():
    def __init__(self):
        # this is the attribute of the aminoacid
        self.age = 0

    def replicate(self):
        # this function sever for replication
        return RightHanded()

    def grow(self):
        # the age will plus one after each cycle, and will dye when it reach it's life span
        self.age += 1


class Environment():
    def __init__(self, environment_burden=10000):
        self.environment_burden = environment_burden

    def initialize(self):
        # this method will create several instances randomly from left hand and right hand

        left_start_number = random.randint(1, 10)
        right_start_number = random.randint(1, 10)

        left_hand_list = [LeftHanded() for i in range(left_start_number)]
        right_hand_list = [RightHanded() for i in range(right_start_number)]

        return left_hand_list, right_hand_list

    def kill(self, instance):
        # this function will kill the existance of on object in the list
        del instance

    def cycle(self, left_hand_list, right_hand_list, maximum_age = 50):
        # this function will go through a cycle for all left_hand_list and right_hand_list
        total_number = len(left_hand_list) + len(right_hand_list)
        if total_number >= self.environment_burden:
            born = False
        else:
            born = True

        # record the the cells that reach it's limitation
        left_hand_death_list = []
        left_hand_born_number = 0
        right_hand_death_list = []
        right_hand_born_number = 0

        for index, left_hand_instance in enumerate(left_hand_list):
            left_hand_instance.grow()
            if left_hand_instance.age >= maximum_age:
                left_hand_death_list.append(index)
            else:
                left_hand_born_number += 1

        for index, right_hand_instance in enumerate(right_hand_list):
            right_hand_instance.grow()
            if right_hand_instance.age >= maximum_age:
                right_hand_death_list.append(index)
            else:
                right_hand_born_number += 1

        # kill the organism that exhausted their life span
        left_hand_list = [value for index, value in enumerate(left_hand_list) if index not in left_hand_death_list]
        right_hand_list = [value for index, value in enumerate(right_hand_list) if index not in right_hand_death_list]

        # give new born to organism
        if born:
            left_hand_list += [LeftHanded() for i in range(left_hand_born_number)]
            right_hand_list += [RightHanded() for i in range(right_hand_born_number)]
        return left_hand_list, right_hand_list

    def accident(self, left_hand_list, right_hand_list, lost_portion=100):
        # it will randomly assign a huge lost based on the whole group and randomly assign it to two different group.

        total_death_number = (len(left_hand_list) + len(right_hand_list)) // lost_portion
        total_death_number = max(1, total_death_number)

        left_death_number = random.choice([i for i in range(total_death_number)])
        right_death_number = total_death_number - left_death_number

        left_death_number = min(len(left_hand_list), left_death_number)
        right_death_number = min(len(right_hand_list), right_death_number)

        left_death_list = random.sample(range(len(left_hand_list)), left_death_number)
        right_death_list = random.sample(range(len(right_hand_list)), right_death_number)

        left_hand_list = [value for index, value in enumerate(left_hand_list) if index not in left_death_list]
        right_hand_list = [value for index, value in enumerate(right_hand_list) if index not in right_death_list]

        return left_hand_list, right_hand_list


def main():
    # the title of the streamlit
    st.title("Is it possible for two different handed amino acid exist in the same time?")

    # input the environment capacity
    environmental_capacity = st.number_input('Please input the Environment Capacity', min_value=1000, value = 10000 )
    cycle = st.number_input("Please input the number of cycle that you want the simulation goes", min_value = 10, value = 100)

    # input the lost portion
    lost_portion = st.number_input("Please input the Lost portion", min_value=1, value=100)
    st.write(
        "PS: it will kill 1/value each cycle, for example, if you input 100, 1/100 of organism will die for each cycle")
    maximum_age = st.number_input("Please input the maximum cycle the organism sustain", min_value=10, value=50)
    st.write("PS: this is the maximum cycles that organism can survived")


    if st.button('Generate Plot'):
        virtual_earth = Environment(environment_burden=environmental_capacity)

        left_hand_list, right_hand_list = virtual_earth.initialize()
        number = pd.DataFrame({
            "left_hand_number": [len(left_hand_list)],
            "right_hand_number": [len(right_hand_list)],
            "totol_number": [len(left_hand_list) + len(right_hand_list)]
        })

        # this is the place where we start our cycle.
        for i in range(cycle):
            left_hand_list, right_hand_list = virtual_earth.cycle(left_hand_list, right_hand_list, maximum_age=maximum_age)
            left_hand_list, right_hand_list = virtual_earth.accident(left_hand_list, right_hand_list,
                                                                     lost_portion=lost_portion)


            number.loc[len(number.index)] = [len(left_hand_list), len(right_hand_list),
                                             len(left_hand_list) + len(right_hand_list)]

        # set up the index
        number = number.reset_index()
        # organize the dataframe
        number_long = number.melt(id_vars="index", var_name="Category", value_name="Count")

        # draw the plot
        sns.lineplot(data=number_long, x="index", y="Count", hue="Category")

        # show the plot
        plt.title('The Changing number of Left and right numbers as Cycle goes')
        plt.legend(title="Category")

        st.pyplot(plt)
        st.write(number)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()