import neo


board = neo.UdooNeo()

board.unexport_all_gpios()

#board.export_all_gpios()


board.export_pwm( 3 )
