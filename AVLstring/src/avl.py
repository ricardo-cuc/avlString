class Node:
    def __init__(self, value, parent=None):
        """
        Every Node has a value, and a height based on how far it is from the root node
        """
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self, List=None):
        self.root = None
        if List:
            for item in List:
                self.insert(item)

    def inorder(self, current_node):
        if current_node:  
            self.inorder(current_node.left)
            print(current_node.value, end=' ')
            self.inorder(current_node.right)

    def max_depth(self, root):
        # Null node has 0 depth.
        if root == None:
            return 0

        # Get the depth of the left and right subtree 
        # using recursion.
        leftDepth = self.max_depth(root.left)
        rightDepth = self.max_depth(root.right)

        # Choose the larger one and add the root to it.
        if leftDepth > rightDepth:
            return leftDepth + 1
        else:
            return rightDepth + 1

    def get_depth(self, node, parent_node):
        """
        gets the value of height 

        which is how far the node is from the root node, given that the root node has a height of 1, and its children has 2
        Ex:

                    O      Height = 1
                  /   \
                 O     O    Height = 2
                / \   / \
               O   O O   O   Height = 3

        """
        if node is None:
            return 0
        return self.max_depth(node)

    def update_heights(self, current_node, depth):
        """

        """
        if current_node is None:
            return 
        current_node.height = depth
        self.update_heights(current_node.left, 1+depth)
        self.update_heights(current_node.right, 1+depth)


    def get_balance_factor(self, node):
        """
        Balance_factor is the difference between the heights of the two child node of the node

        Rebalancing occurs when the balance_factor is greater than a difference of 1 (or) less than a difference of -1

        usage: balance_factor = get_balance_factor(node)
        which is left_child_height - right_child_height

        If balanced, balance_factor = -1/0/1:
                O           O          O         O      
               / \         / \        / \       / \ 
              O   O       O   O      O   O     O   O
                         / \        /               \ 
                        O   O      O                 O   

        If balance_factor > 1:
                O    <--- Node
               / \ 
              O   O   Height = 2
             / \ 
            O   O     Height = 3
           / \ 
          O   O       Height = 4  
            Difference of L and R = 2 (4-2)

        If balance_factor < 1:
                O   <--- Node
               / \ 
              O   O        Height = 2
                 / \        
                O   O      Height = 3
                   / \ 
                  O   O    Height = 4
            Difference of L and R = -2 (2-4)


        """
        if node is None:
            return 
        return self.get_depth(node.left, node) - self.get_depth(node.right, node)


    def rotate_right(self, y):
        """
        Rotates right
        Ex:

              y                               x
             / \     Right Rotation          /  \
            x   T3   - - - - - - - >        T1   y 
           / \                                  / \
          T1  T2                              T2  T3

        so only 2 things changed
        the left child of y became T2
        and the right child of x became y

        """
        # Rotation
        parent = y.parent

        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        if T2:
            T2.parent = y
        x.parent = parent


        if parent is None:
            self.root = x
        if parent.left == y:
            parent.left = x
        elif y.parent.right == y:
            parent.right = x

        # Updating Heights
        self.update_heights(x, y.height)

    def rotate_left(self, x):
        """
        Rotates left
        Ex:

              y                               x
             / \                             /  \
            x   T3                          T1   y 
           / \       < - - - - - - -            / \
          T1  T2     Left Rotation            T2  T3

        """
        # Rotation
        parent = x.parent
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        if T2:
            T2.parent = x
        y.parent = parent

        if parent is None:
            self.root = y 
        elif parent.left == x:
            parent.left = y
        elif y.parent.right == x:
            parent.right = y

        # Updating Heights
        self.update_heights(y, x.height)

    def recursive_balancing(self, current_node, value):
        if current_node is None:
            return

        # Getting the balance factor, which shows if the tree is balanced or not after insertion, by the difference of the heights between the left and right children of the node
        balance_factor = self.get_balance_factor(current_node)
        print(balance_factor)

        # Checks if the node is unbalanced, and if it is, perform one of the 4 cases
        # Case 1: Left Left
        if balance_factor > 1 and current_node.left:
            if value < current_node.left.value:
                self.rotate_right(current_node)

        # Case 2: Right Right
        if balance_factor < -1 and current_node.right:
            if value > current_node.right.value:
                self.rotate_left(current_node)

        # Case 3: Left Right
        if balance_factor > 1 and current_node.left:
            if value > current_node.left.value:
                self.rotate_left(current_node.left)
                self.rotate_right(current_node)

        # Case 4: Right Left
        if balance_factor < -1 and current_node.right:
            if value < current_node.right.value:
                self.rotate_right(current_node.right)
                self.rotate_left(current_node)

        self.recursive_balancing(current_node.parent, value)

    def insert(self, value):
        NewNode = Node(value)
        current_node = self.root

        # Traversing through the Tree till we find the right place to put the value
        if current_node is None:
            self.root = NewNode
        else:
            while True:
                if value < current_node.value:
                    NewNode.parent = current_node
                    #Left
                    if not current_node.left:
                        current_node.left = NewNode
                        break
                    NewNode.parent = current_node
                    current_node = current_node.left
                else:
                    NewNode.parent = current_node
                    #Right
                    if not current_node.right:
                        current_node.right = NewNode
                        break
                    NewNode.parent = current_node
                    current_node = current_node.right

            # Giving the new node a value of height based on how far he is from root node
            NewNode.height = 1 + current_node.height

            # Recursive balancing
            self.recursive_balancing(current_node, value)

            
