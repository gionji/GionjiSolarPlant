import tornado.ioloop
import tornado.web

import database
import relayBox as rb


class LastData( tornado.web.RequestHandler ):
    def get(self):
        #self.write("Hello, world")
        
        self.write(database.getLastData())


class Plugs( tornado.web.RequestHandler ):
    def get(self):
        self.write("plug_id: a b i e --- state: 0 1")
    
    
    def post(self):
        plug_id = self.get_argument('plug_id')
        state  = self.get_argument('state')

        self.write( "plug_id: " + str(plug_id) + "/nstate: " + str(state) )


        if plug_id == rb.PLUG_A_ID:
            if state == rb.STATE_ON:
                rb.enablePlugA()
                print( "Turn on plug A" )
            elif state == rb.STATE_OFF:
                rb.disablePlugA()
                print( "Turn off plug A" )
        
        elif plug_id == rb.PLUG_B_ID:
            if state == rb.STATE_ON:
                rb.enablePlugB()
                print( "Turn on plug B" )
            elif state == rb.STATE_OFF:
                rb.disablePlugB()
                print( "Turn off plug B" )

        elif plug_id == rb.INVERTER_ID:
            if state == rb.STATE_ON:
                rb.enableInverter()
                print( "Turn on INVERTER" )
            elif state == rb.STATE_OFF:
                rb.disableInverter()
                print( "Turn off plug invereter" )


        elif plug_id == rb.EXTERNAL_SOURCE_ID:
            if state == rb.STATE_ON:
                rb.enableExternalPower()
                print( "Turn on external power subbly" )
            elif state == rb.STATE_OFF:
                rb.disableExternalPower()
                print( "Turn on solar panel" )

        


class User(tornado.web.RequestHandler):

    def get(self):
        form = """<form method="post">
        <input type="text" name="username"/>
        <input type="text" name="designation"/>
        <input type="submit"/>
        </form>"""
        self.write(form)

    def post(self):
        start    = self.get_argument('start')
        end      = self.get_argument('end')

        database.get

        self.write("Wow " + username + " you're a " + designation)





application = tornado.web.Application([
    (r"/last/", LastData),
    (r"/user/", User),
    (r"/relaybox/", Plugs),
])




if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
