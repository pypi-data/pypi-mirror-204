import cv2
import numpy as np


def compute_displacement(point, pointf):
    """To compute a displacement between two point arrays"""
    assert len(point)==len(pointf)
    values = []
    for i, pt0 in enumerate(point):
        pt1 = pointf[i]
        values.append((pt1[0]-pt0[0], pt1[1]-pt0[1]))
    return values

def compute_disp_and_remove_rigid_transform(p1, p2):
     """Computes the displacement between two point sets and removes rigid transform.

     This function computes the optimal rotation and translation between two sets of 
     points (p1 and p2) using Singular Value Decomposition (SVD). The function also 
     removes the rigid transform between the point sets and returns the displacement 
     between them.

     Args:
          p1 (numpy.array): An Nx2 numpy array representing the first set of 2D points.
          p2 (numpy.array): An Nx2 numpy array representing the second set of 2D points.

     Returns:
          numpy.array: An Nx2 numpy array representing the displacement between the two 
                         point sets after removing the rigid transform.

     Raises:
          AssertionError: If the lengths of the input point sets do not match.
     """ 
     A = []
     B = []
     removed_indices = []
     for i in range(len(p1)):
          if np.isnan(p1[i][0]):
               assert np.isnan(p1[i][0]) and np.isnan(p1[i][1]) and np.isnan(p2[i][0]) and np.isnan(p2[i][1])
               removed_indices.append(i)
          else:
               A.append(p1[i])
               B.append(p2[i])
          
     A = np.matrix(A)
     B =  np.matrix(B)
     assert len(A) == len(B)
     N = A.shape[0]; # total points
     
     centroid_A = np.mean(A, axis=0)
     centroid_B = np.mean(B, axis=0)
    
     # centre the points
     AA = np.matrix(A - np.tile(centroid_A, (N, 1)))
     BB = np.matrix(B - np.tile(centroid_B, (N, 1)))

     # dot is matrix multiplication for array
     H = np.transpose(AA) * BB
     U, S, Vt = np.linalg.svd(H)
     R = Vt.T * U.T

     # special reflection case
     if np.linalg.det(R) < 0:
          print("Reflection detected")
          Vt[2,:] *= -1
          R = Vt.T * U.T

     n = len(A)
     T = -R*centroid_A.T + centroid_B.T
     A2 = (R*A.T) + np.tile(T, (1, n))
     A2 = np.array(A2.T)
     out = []
     j = 0
     for i in range(len(p1)):
          if np.isnan(p1[i][0]):
               out.append(p1[i])
          else:
               out.append(A2[j])
               j = j + 1
     out = np.array(out)
     return compute_displacement(p2, out)



def remove_point_outside(points, area, *args, **kwargs):
    """
    Removes points that are outside the specified rectangular area.

    Args:
        points (List[Tuple[float, float]]): A list of points, each point represented as a tuple (x, y).
        area (List[Tuple[float, float]]): The area of interest, represented as two tuples
            [(top_left_x, top_left_y), (bottom_right_x, bottom_right_y)].
        *args: Additional arguments (not used in this function).
        **kwargs: Additional keyword arguments. Accepts 'shape' keyword (not used in this function).

    Returns:
        np.array: A NumPy array containing the filtered points that are inside the specified area.
    """
    # shape = 'box' if 'shape' not in kwargs else kwargs['shape']
    xmin = area[0][0]
    xmax = area[1][0]
    ymin = area[0][1]
    ymax = area[1][1]
    res = []
    for p in points:
        x = p[0]
        y = p[1]
        if (x >= xmin) and (x <= xmax) and (y >= ymin) and (y <= ymax):
            res.append(p)
    return np.array(res)


#%%[markdown]
# # Area selector

#%%

class AreaSelector:
    '''This class uses opencv to select an area or interest.
    '''
    def __init__(self, PreliminaryImage):
        self.area = []
        self.cropping = False
        self.image = cv2.putText(PreliminaryImage, "Pick the area of interest (left click + move mouse) and press 'c' button to continue", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),4)

    def pick_area_of_interest(self):
        """
        Picks area of interest from an image if data are not selected.

        Returns:
            list: A list of tuples representing the coordinates of the area of interest.
        """
        clone = self.image.copy()
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', self.image.shape[1], self.image.shape[0])
        cv2.setMouseCallback("image", self.click_and_crop)

        while True:
            cv2.imshow("image", self.image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                self.image = clone.copy()
            elif key == ord("c"):
                print(f'The area of interest is {self.area}')
                break
        return self.area

    def click_and_crop(self, event, x, y, flags, param):
        """
        Handles mouse events for selecting the area of interest.

        Args:
            event (int): OpenCV event type.
            x (int): X-coordinate of the mouse event.
            y (int): Y-coordinate of the mouse event.
            flags (int): Event flags.
            param (any): Extra parameters.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.area = [(x, y)]
            self.cropping = True

        elif event == cv2.EVENT_LBUTTONUP:
            self.area.append((x, y))
            self.cropping = False

            new_image = cv2.rectangle(self.image, self.area[0], self.area[1], (0, 255, 0), 2)
            cv2.imshow('image', new_image)
