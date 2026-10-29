import json
import re
import pprint

def chunk_technical_specification(file_path, chunk_size=300, overlap=50):
    """
    Reads a technical specification document, extracts sections based on 
    subsystem markers, and splits them into overlapping chunks with metadata 
    tailored for RAG (Retrieval-Augmented Generation) vector databases.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"[OK]: Successfully loaded spec file: {file_path}")
    except FileNotFoundError:
        print(f"[ERROR]: Specification file not found at: {file_path}")
        return []
    except UnicodeDecodeError as err:
        print(f"[ERROR]: Encoding error: {err}")
        return []

    # Split content by structural headers or subsystem brackets (e.g., [TRACTION], [DOORS])
    sections = re.split(r'\n(?=[#\[])', content)
    
    chunks = []
    for section in sections:
        section = section.strip()
        # Guard clause: skip empty sections resulting from splitting
        if not section:
            continue
            
        # Extract subsystem/chapter name as metadata for better LLM retrieval
        header_match = re.match(r'^(?:#\s*|\[)([^\]#\n]+)(?:\]|\n)', section)
        subsystem = header_match.group(1).strip() if header_match else "GENERAL_SYSTEM"

        # Sliding window chunking for long technical sections
        words = section.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            
            # Keep chunks that contain meaningful technical text
            if len(chunk_text.strip()) > 30:
                chunks.append({
                    "subsystem": subsystem,
                    "content": chunk_text,
                    "token_approx": len(chunk_words)
                })

    return chunks

if __name__ == "__main__":
    print("--- Starting AI Spec Chunking Pipeline ---\n")
    
    spec_filename = "train_requirements_spec.txt"
    
    # 1. Create a sample technical requirement document for demonstration
    try:
        with open(spec_filename, "w", encoding="utf-8") as dummy:
            dummy.write("[TRACTION_INVERTER]\n")
            dummy.write("The traction inverter must maintain thermal stability up to 85°C ambient temperature. ")
            dummy.write("It communicates via CAN-bus protocol with a refresh rate of 10ms under normal operation.\n\n")
            dummy.write("[DOOR_SYSTEM]\n")
            dummy.write("Emergency mechanical release must operate under a maximum manual force of 150N. ")
            dummy.write("Obstruction detection sensors must trigger a door reversal within 200ms of impact.")
    except OSError:
        pass

    # 2. Process the specification into structured chunks ready for vector embedding
    structured_chunks = chunk_technical_specification(spec_filename)
    
    print("\n--- Generated RAG Chunks Preview ---")
    pprint.pprint(structured_chunks)

    # 3. Export to JSON for vector DB ingestion or agent pipeline
    output_json = "spec_vector_chunks.json"
    try:
        with open(output_json, "w", encoding="utf-8") as out:
            json.dump(structured_chunks, out, indent=4, ensure_ascii=False)
        print(f"\n[SUCCESS]: Structured chunks successfully exported to {output_json}")
    except (TypeError, OSError) as err:
        print(f"[FAIL]: Could not save JSON file: {err}")
