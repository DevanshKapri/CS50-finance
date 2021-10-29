import numpy as np
import matplotlib.pyplot as plt

city_list = np.array([[4,6],[3,9],[5,8],[7,2]])

solution = np.arange(city_list.shape[0])
city_locations = np.concatenate((np.array([city_list[solution[i]] for i in range(len(solution))])))

plt.scatter(city_list[:,0],city_list[:,1])
plt.plot(city_locations[:,0],city_locations[:,1])
plt.title("Initial solutions")
plt.show()

distance_calculation = lambda r,c: np.sum([np.linalg.norm(c[r[p]] - c[r[p-1]]) for p in range(len(solution))])
swap_algorithm = lambda r,i,k: np.concatenate((r[0:i],r[k:-len(r)+i - 1 : -1],r[k+1:len(r)]))
current_best_distance = distance_calculation(solution,city_list)

for swap1 in range(1,len(solution)-2):
    for swap2 in range(swap1 + 1 , len(solution)):
        new_solution = swap_algorithm(solution,swap1,swap2)
        new_distance = distance_calculation(new_solution,city_list)
        if new_distance < current_best_distance:
            solution = new_solution
            current_best_distance = new_distance

plt.figure()
city_locations = np.concatenate((np.array([city_list[solution[i]] for i in range(len(solution))])))
plt.scatter(city_list[:,0],city_list[:,1])
plt.plot(city_locations[:,0],city_locations[:,1])
plt.title("Final solution")
plt.show()

print('final solution',solution)
print('best distance ',distance_calculation(solution,city_list))
