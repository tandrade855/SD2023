from server_skeleton import *

def main():
    gm = GameMechanics()
    skeleton = SkeletonServer(gm)
    skeleton.run()

main()