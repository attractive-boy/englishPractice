from flask import Blueprint, request, jsonify, session
from models import Scenario, db, ChatMessage
from spark_ai import conversation
from uuid import uuid4

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/messages', methods=['POST'])
def add_message():
    data = request.json
    
    # 获取必要的数据
    user_id = session.get('user_id')
    scenario_id = data.get('selectedScene')
    difficulty = data.get('selectedDifficulty')
    conversation_id = session.get('conversation_id', str(uuid4()))  # Generate a new conversation ID if not present
    
    # 将新的conversation_id存入session
    session['conversation_id'] = conversation_id
    
    # 根据 scenario_id.name 和 difficulty 找到 scenario 对象
    scenario = Scenario.query.filter_by(name=scenario_id.get('name'), difficulty=difficulty).first()
    content = data.get('content')
    timestamp = data.get('timestamp')

    # 创建新的聊天消息记录
    new_message = ChatMessage(
        user_id=user_id,
        scenario_id=scenario.scenario_id,
        difficulty=difficulty,
        content=content,
        conversation_id=conversation_id,
        is_user=True  # This message is from the user
    )
    
    # 添加到数据库并提交
    db.session.add(new_message)
    db.session.commit()

    # Retrieve all previous messages in the conversation
    previous_messages = ChatMessage.query.filter_by(conversation_id=conversation_id).order_by(ChatMessage.timestamp).all()
    
    # Construct the context with all previous messages
    context = [{"role": "system", "content": scenario.prompt}]
    for message in previous_messages:
        role = "user" if message.is_user else "assistant"
        context.append({"role": role, "content": message.content})
    # Append the new user message
    context.append({"role": "user", "content": content})

    # Generate system response
    ai_response = conversation(context)

    # Extract the AI response content
    system_response_content = ai_response.generations[0][0].text

    # 创建新的聊天消息记录，用于AI的响应
    ai_message = ChatMessage(
        user_id=user_id,
        scenario_id=scenario.scenario_id,
        difficulty=difficulty,
        content=system_response_content,
        conversation_id=conversation_id,
        is_user=False  # This message is from the AI
    )
    
    # 添加AI的响应到数据库并提交
    db.session.add(ai_message)
    db.session.commit()

    return jsonify({
        "user_message": new_message.to_dict(),
        "ai_message": ai_message.to_dict()
    }), 201


@chat_bp.route('/messages', methods=['GET'])
def get_messages():
    user_id = session.get('user_id')
    conversation_id = session.get('conversation_id')  # Ensure this is set appropriately in your session

    if not conversation_id:
        return jsonify({"error": "Conversation ID not found"}), 400

    messages = ChatMessage.query.filter_by(conversation_id=conversation_id).order_by(ChatMessage.timestamp).all()
    return jsonify([message.to_dict() for message in messages])

