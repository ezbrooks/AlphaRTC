#include "cmdinfer.h"

#include "modules/third_party/statcollect/json.hpp"
#include "third_party/cppzmq/zmq.hpp"

#include <string>
#include <iostream>

#ifndef _WIN32
#include <unistd.h>
#else
#include <windows.h>
#endif

// send c++ data to python
void cmdinfer::ReportStates(
    std::uint64_t sendTimeMs,
    std::uint64_t receiveTimeMs,
    std::size_t payloadSize,
    std::uint8_t payloadType,
    std::uint16_t sequenceNumber,
    std::uint32_t ssrc,
    std::size_t paddingLength,
    std::size_t headerLength) {

    nlohmann::json j;
    j["send_time_ms"] = sendTimeMs;
    j["arrival_time_ms"] = receiveTimeMs;
    j["payload_type"] = payloadType;
    j["sequence_number"] = sequenceNumber;
    j["ssrc"] = ssrc;
    j["padding_length"] = paddingLength;
    j["header_length"] = headerLength;
    j["payload_size"] = payloadSize;

	const auto json_str = j.dump();

    zmq::context_t context;
    zmq::socket_t socket (context, ZMQ_REP);
    socket.bind ("tcp://*:5555");

    // Test sending sample data before converting to the actual message
	// TODO: modify to send the actual data
    zmq::message_t reply (5);
    memcpy (reply.data (), "10000", 5);
    socket.send (reply, zmq::send_flags::none);

}

// receive data from python back to c++
float cmdinfer::GetEstimatedBandwidth() {

	zmq::context_t context;
    zmq::socket_t socket (context, ZMQ_REP);
    socket.bind ("tcp://*:5555");

    // This will be the data sent back from python
    zmq::message_t request;
    socket.recv (request, zmq::recv_flags::none);

    // TEST: send dummy values back
	float result = 100000.0;
    return(result);
}
