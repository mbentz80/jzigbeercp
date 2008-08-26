#include "ServerSocket.h"
#include "SocketException.h"
#include <string>

int main( int argc, int argv[] )

  try
    {
      // Create the server socket
             ServerSocket server ( 30000 );
      
      //             // rest of code -
      //                   // accept connection, handle request, etc...
      //
    }
   catch ( SocketException& e ) {
         std::cout << "Exception was caught:" << e.description() << "\nExiting.\n";
   }
      //
   return 0;
}
