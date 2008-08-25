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
}

struct JAUSMessage {
	JAUSHeader head;
	unsigned char[4080] message;
}

class JAUSMessage {
	//!A JAUS Message
	/*!This class defines the standard JAUS message, along with its standards*/
	private JAUSHeader head;
	bool setPriority(unsigned char priority) {
		if(priority > 16) {
			return false;
		}
		else {
			head.message_properties=head.message_properties & 0b1111111111110000;
			head.message_properties=head.message_properties | priority;
			return true;
		}
	}
	bool setACKNAK(unsigned char origin, unsigned char ack) {
		head.message_properties=head.message_properties & 0b1111111111001111;	//Clear the ACK
		if(origin) {
			

		}
	}
}