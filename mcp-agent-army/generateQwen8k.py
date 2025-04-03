import os
import subprocess
import tempfile

def generate_qwen8k_model():
    """Generate qwen2.5:14b-instruct-8k model variant in Ollama"""
    try:
        # Create temporary Modelfile
        modelfile_content = """FROM qwen2.5:14b
PARAMETER num_ctx 8192"""
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.Modelfile') as tmp:
            tmp.write(modelfile_content)
            tmp_path = tmp.name
        
        try:
            # Copy to container and create model
            subprocess.run([
                'docker', 'cp', tmp_path, 
                'ollama:/root/Qwen8k.Modelfile'
            ], check=True)
            
            subprocess.run([
                'docker', 'exec', 'ollama', 
                'ollama', 'create', 
                'qwen2.5:14b-instruct-8k', 
                '-f', '/root/Qwen8k.Modelfile'
            ], check=True)
            
            print("Successfully created qwen2.5:14b-instruct-8k model")
            
        finally:
            # Clean up
            os.unlink(tmp_path)
            subprocess.run([
                'docker', 'exec', 'ollama',
                'rm', '-f', '/root/Qwen8k.Modelfile'
            ], check=False)
            
    except subprocess.CalledProcessError as e:
        print(f"Error creating model: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    generate_qwen8k_model()
