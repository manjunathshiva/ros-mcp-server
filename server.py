#!/usr/bin/env python3
import asyncio
import json
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import roslibpy

# Connect to ROS in your Ubuntu VM
ros = roslibpy.Ros(host='192.168.64.2', port=9090)

app = Server("ros-mcp-server")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_topics",
            description="List all available ROS topics",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_topic_info",
            description="Get information about a specific ROS topic",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic_name": {
                        "type": "string",
                        "description": "Name of the ROS topic"
                    }
                },
                "required": ["topic_name"]
            }
        ),
        types.Tool(
            name="publish_message",
            description="Publish a message to a ROS topic",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic_name": {"type": "string"},
                    "message_type": {"type": "string"},
                    "message_data": {"type": "object"}
                },
                "required": ["topic_name", "message_type", "message_data"]
            }
        ),
        types.Tool(
            name="list_nodes",
            description="List all available ROS nodes",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_node_info",
            description="Get information about a specific ROS node",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_name": {
                        "type": "string",
                        "description": "Name of the ROS node"
                    }
                },
                "required": ["node_name"]
            }
        ),
        types.Tool(
            name="list_services",
            description="List all available ROS services",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_service_info",
            description="Get information about a specific ROS service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the ROS service"
                    }
                },
                "required": ["service_name"]
            }
        ),
        types.Tool(
            name="call_service",
            description="Call a ROS service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {"type": "string"},
                    "service_type": {"type": "string"},
                    "service_args": {"type": "object"}
                },
                "required": ["service_name", "service_type", "service_args"]
            }
        ),
        types.Tool(
            name="get_param",
            description="Get a ROS parameter value",
            inputSchema={
                "type": "object",
                "properties": {
                    "param_name": {
                        "type": "string",
                        "description": "Name of the ROS parameter"
                    }
                },
                "required": ["param_name"]
            }
        ),
        types.Tool(
            name="set_param",
            description="Set a ROS parameter value",
            inputSchema={
                "type": "object",
                "properties": {
                    "param_name": {"type": "string"},
                    "param_value": {"type": "string"}
                },
                "required": ["param_name", "param_value"]
            }
        ),
        types.Tool(
            name="list_params",
            description="List all available ROS parameters",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="subscribe_topic",
            description="Subscribe to a ROS topic and get recent messages",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic_name": {
                        "type": "string",
                        "description": "Name of the ROS topic"
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Timeout in seconds to listen for messages",
                        "default": 5.0
                    }
                },
                "required": ["topic_name"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "list_topics":
            topics = ros.get_topics()
            return [types.TextContent(type="text", text=f"Available topics: {topics}")]
        
        elif name == "get_topic_info":
            topic_name = arguments["topic_name"]
            topic_type = ros.get_topic_type(topic_name)
            return [types.TextContent(type="text", text=f"Topic {topic_name} type: {topic_type}")]
        
        elif name == "publish_message":
            topic_name = arguments["topic_name"]
            message_type = arguments["message_type"]
            message_data = arguments["message_data"]
            
            publisher = roslibpy.Topic(ros, topic_name, message_type)
            publisher.publish(roslibpy.Message(message_data))
            return [types.TextContent(type="text", text=f"Published message to {topic_name}")]
        
        elif name == "list_nodes":
            nodes = ros.get_nodes()
            return [types.TextContent(type="text", text=f"Available nodes: {nodes}")]
        
        elif name == "get_node_info":
            node_name = arguments["node_name"]
            # Get node info (publications, subscriptions, services)
            node_details = ros.get_node_details(node_name)
            return [types.TextContent(type="text", text=f"Node {node_name} details: {node_details}")]
        
        elif name == "list_services":
            services = ros.get_services()
            return [types.TextContent(type="text", text=f"Available services: {services}")]
        
        elif name == "get_service_info":
            service_name = arguments["service_name"]
            service_type = ros.get_service_type(service_name)
            return [types.TextContent(type="text", text=f"Service {service_name} type: {service_type}")]
        
        elif name == "call_service":
            service_name = arguments["service_name"]
            service_type = arguments["service_type"]
            service_args = arguments["service_args"]
            
            service = roslibpy.Service(ros, service_name, service_type)
            request = roslibpy.ServiceRequest(service_args)
            result = service.call(request)
            return [types.TextContent(type="text", text=f"Service call result: {result}")]
        
        elif name == "get_param":
            param_name = arguments["param_name"]
            param = roslibpy.Param(ros, param_name)
            value = param.get()
            return [types.TextContent(type="text", text=f"Parameter {param_name} value: {value}")]
        
        elif name == "set_param":
            param_name = arguments["param_name"]
            param_value = arguments["param_value"]
            param = roslibpy.Param(ros, param_name)
            param.set(param_value)
            return [types.TextContent(type="text", text=f"Set parameter {param_name} to {param_value}")]
        
        elif name == "list_params":
            params = ros.get_params()
            return [types.TextContent(type="text", text=f"Available parameters: {params}")]
        
        elif name == "subscribe_topic":
            topic_name = arguments["topic_name"]
            timeout = arguments.get("timeout", 5.0)
            
            messages = []
            listener = roslibpy.Topic(ros, topic_name)
            
            def message_callback(message):
                messages.append(message)
            
            listener.subscribe(message_callback)
            
            # Wait for messages
            await asyncio.sleep(timeout)
            listener.unsubscribe()
            
            if messages:
                return [types.TextContent(type="text", text=f"Received {len(messages)} messages from {topic_name}: {messages[-5:]}")]  # Last 5 messages
            else:
                return [types.TextContent(type="text", text=f"No messages received from {topic_name} within {timeout} seconds")]
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing {name}: {str(e)}")]

async def main():
    ros.run()
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ros-mcp-server",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())