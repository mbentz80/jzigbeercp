/***************************************************************************
 *   Copyright (C) 2008 by mbentz,,,   *
 *   mbentz@argon   *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU Library General Public License as       *
 *   published by the Free Software Foundation; either version 2 of the    *
 *   License, or (at your option) any later version.                       *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this program; if not, write to the                 *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/


#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <iostream>
#include <cstdlib>

using namespace std;
struct JAUSHeader {	//16 Bytes of the JAUS Header
	unsigned short message_properties;
	unsigned short command_code;
	unsigned char dest_inst_id;
	unsigned char dest_comp_id;
	unsigned char dest_node_id;
	unsigned char dest_subs_id;
	unsigned char src_inst_id;
	unsigned char src_comp_id;
	unsigned char src_node_id;
	unsigned char src_subs_id;
	unsigned short data_ctrl;
	unsigned short seq_num;
};

class JAUSMessage {
	//!A JAUS Message
	/*!This class defines the standard JAUS message, along with its standards*/
	private: JAUSHeader head;
	public: 
		bool setPriority(unsigned char priority) {
		if(priority > 16) {
			return false;
		}
		else {
			head.message_properties=head.message_properties & 0xFFF0;
			head.message_properties=head.message_properties | priority;
			return true;
		}
	}
	bool setACKNAK(unsigned char origin, unsigned char ack) {
	head.message_properties=head.message_properties & 0xFFBF;	//Clear the ACK
	if(origin) {
		if(ack) {
			head.message_properties= head.message_properties | 0xFFBF;	//Origin, ACK
		}
		else {
			head.message_properties= head.message_properties | 0xFFCF;	//Origin, not ACK
		return true;

		}
	}
	else
		return false;
}
};

int main(int argc, char *argv[])
{
  unsigned short test;
  JAUSMessage blah;
  blah.setPriority(3);
  test = 14;
  test = test | 3;
cout << "Hello, world!" << endl;
cout << test << endl;

  return EXIT_SUCCESS;
}
