import streamlit as st


with open("policy.txt", "r") as file:
    policy_data = file.read()


st.title("Return & Refund Assistant")


st.write("### Policy Loaded:")
st.write(policy_data)


st.write("Ask me anything about returns and refunds!")

question = st.text_input("Enter your question:")

if st.button("Submit"):
    if question:
        question = question.lower()
        lines = policy_data.split("\n")

        if "return" in question:
            response = "\n".join([line for line in lines if "return" in line.lower()])
        elif "refund" in question:
            response = "\n".join([line for line in lines if "refund" in line.lower()])
        elif "damaged" in question:
            response = "\n".join([line for line in lines if "damaged" in line.lower()])
        else:
            response = "Sorry, I can only answer return/refund questions."

        st.write("### Response:")
        st.write(response)
    else:
        st.write("Please enter a question.")