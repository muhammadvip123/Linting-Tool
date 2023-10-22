module adder(
    input [3:0] in1,
    input [3:0] in2,
    output reg [3:0] out,out2,out3,out4,out1,out5
);
    wire  [1:0]  internOut;

    assign internOut = (in1*in2*in1);

    localparam [3:0]      idle=4'b0000,             //s0
                      blance_check=4'b0001,     //s1
					  withdraw=4'b0010,         //s2
					  deposit=4'b0011,          //s3
					  transfer=4'b0100, 		//s4
					  exit=4'b0101,             //s5
					  new_pass=4'b0110,         //s6
					  lang_used=4'b0111,        //s7
					  scan_card=4'b1000,         //s8
					  enter_pass=4'b1001,       //s9
					  option_select=4'b1010,    //s10 
					  anything_else=4'b1011;    //s11

    always@(*) begin
        out1 = in2 ==in1;
        out2 = in1+in1;
        out3 = in2*in1;
        if(in1==in2)
        begin
            if(^in2)
                out = |in1;
            else
                out = |in2;
            out = &(in1*in2);
            out3 = |(in1+in2);
            if(in1 >= in2) begin
                out4 = in1/in2;
            end
            else if(in1&in2)
                begin
                    out=|in2;
                    out2 =& in2;
                end
            else
                out3 = | ( in1+in2 );
        end
        else if(in1>in2)
            out = in1>>2;
        else begin
            out2= ^(in1*in2);
            out4 = in1<<2;
        end
        out4 = in1&in2&out3;
        case(in1&in2)
        blance_check : begin
                    out4 = in1<<2;
                    out2 = in2*in1;
        end
        default: out4 = 0;
        endcase
    end
    always@(*) begin
        out1 = in2 ==in1;
        out2 = in1+in1;
        out5 = in2*in1;
        if(in1==in2)
        begin
            if(^in2)
                out = |in1;
            else
                out = |in2;
            out = &(in1*in2);
            out5 = |(in1+in2);
            if(in1 >= in2) begin
                out4 = in1/in2;
            end
            else if(in1&in2)
                begin
                    out=|in2;
                    out2 =& in2;
                end
            else
                out5 = | ( in1+in2 );
        end
        else if(in1>in2)
            out = in1>>2;
        else begin
            out2= ^(in1*in2);
            out4 = in1<<2;
        end
        out4 = in1&in2&out3;
        case(in1&in2)
        blance_check : begin
                    out4 = in1<<2;
                    out2 = in2*in1;
        end
        default: out4 = 0;
        endcase
    end

        always@(*) begin
        out1 = in2 ==in1;
        out2 = in1+in1;
        out5 = in2*in1;
        if(in1==in2)
        begin
            if(^in2)
                out = |in1;
            else
                out = |in2;
            out = &(in1*in2);
            out5 = |(in1+in2);
            if(in1 >= in2) begin
                out4 = in1/in2;
            end
            else if(in1&in2)
                begin
                    out=|in2;
                    out2 =& in2;
                end
            else
                out5 = | ( in1+in2 );
        end
        else if(in1>in2)
            out = in1>>2;
        else begin
            out2= ^(in1*in2);
            out4 = in1<<2;
        end
        out4 = in1&in2&out3;
        case(in1&in2)
        blance_check : begin
                    out4 = in1<<2;
                    out2 = in2*in1;
                    out3 = in2*in1;
        end
        default: out4 = 0;
        endcase
    end
endmodule

    