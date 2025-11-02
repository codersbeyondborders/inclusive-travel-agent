#!/usr/bin/env python3
"""
Deployment script for Cloud Run deployment of the Inclusive Travel Agent.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"Error running command: {command}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    
    return result


def check_prerequisites():
    """Check that required tools and configurations are available."""
    print("Checking prerequisites...")
    
    # Check if gcloud is installed
    result = run_command("gcloud version", check=False)
    if result.returncode != 0:
        print("Error: gcloud CLI is not installed or not in PATH")
        print("Please install gcloud CLI: https://cloud.google.com/sdk/docs/install")
        sys.exit(1)
    
    # Check if Docker is installed
    result = run_command("docker --version", check=False)
    if result.returncode != 0:
        print("Error: Docker is not installed or not in PATH")
        print("Please install Docker: https://docs.docker.com/get-docker/")
        sys.exit(1)
    
    # Check if authenticated with gcloud
    result = run_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'", check=False)
    if not result.stdout.strip():
        print("Error: Not authenticated with gcloud")
        print("Please run: gcloud auth login")
        sys.exit(1)
    
    print("✓ Prerequisites check passed")


def setup_project(project_id: str, region: str = "us-central1"):
    """Set up the Google Cloud project for deployment."""
    print(f"Setting up project: {project_id}")
    
    # Set the project
    run_command(f"gcloud config set project {project_id}")
    
    # Enable required APIs
    apis = [
        "cloudbuild.googleapis.com",
        "run.googleapis.com",
        "containerregistry.googleapis.com",
        "aiplatform.googleapis.com"
    ]
    
    for api in apis:
        print(f"Enabling API: {api}")
        run_command(f"gcloud services enable {api}")
    
    # Set default region for Cloud Run
    run_command(f"gcloud config set run/region {region}")
    
    print("✓ Project setup completed")


def build_and_deploy(project_id: str, region: str = "us-central1", use_cloud_build: bool = True):
    """Build and deploy the application to Cloud Run."""
    print("Building and deploying application...")
    
    if use_cloud_build:
        # Use Cloud Build for building and deployment
        print("Using Cloud Build for deployment...")
        run_command(f"gcloud builds submit --config cloudbuild.yaml")
    else:
        # Local build and deploy
        print("Building locally and deploying...")
        
        # Build the Docker image
        image_name = f"gcr.io/{project_id}/inclusive-travel-agent:latest"
        run_command(f"docker build -t {image_name} .")
        
        # Push to Container Registry
        run_command(f"docker push {image_name}")
        
        # Deploy to Cloud Run
        deploy_cmd = f"""
        gcloud run deploy inclusive-travel-agent \
            --image {image_name} \
            --region {region} \
            --platform managed \
            --allow-unauthenticated \
            --memory 2Gi \
            --cpu 2 \
            --max-instances 10 \
            --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=0 \
            --set-env-vars INCLUSIVE_TRAVEL_AGENT_SCENARIO=inclusive_travel_agent/profiles/itinerary_accessible_default.json
        """
        run_command(deploy_cmd)
    
    print("✓ Deployment completed")


def get_service_url(project_id: str, region: str = "us-central1") -> str:
    """Get the URL of the deployed Cloud Run service."""
    result = run_command(
        f"gcloud run services describe inclusive-travel-agent --region {region} --format 'value(status.url)'",
        check=False
    )
    
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    else:
        return f"https://inclusive-travel-agent-{project_id}.a.run.app"


def test_deployment(service_url: str):
    """Test the deployed service."""
    print(f"Testing deployment at: {service_url}")
    
    # Test health endpoint
    import requests
    try:
        response = requests.get(f"{service_url}/health", timeout=30)
        if response.status_code == 200:
            print("✓ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test agent info endpoint
    try:
        response = requests.get(f"{service_url}/agent/info", timeout=30)
        if response.status_code == 200:
            info = response.json()
            print(f"✓ Agent info retrieved: {info['total_sub_agents']} sub-agents")
        else:
            print(f"❌ Agent info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Agent info failed: {e}")


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description="Deploy Inclusive Travel Agent to Cloud Run")
    parser.add_argument("--project-id", required=True, help="Google Cloud Project ID")
    parser.add_argument("--region", default="us-central1", help="Cloud Run region")
    parser.add_argument("--setup-only", action="store_true", help="Only setup project, don't deploy")
    parser.add_argument("--local-build", action="store_true", help="Build locally instead of using Cloud Build")
    parser.add_argument("--skip-test", action="store_true", help="Skip deployment testing")
    
    args = parser.parse_args()
    
    print("🚀 Starting Inclusive Travel Agent Cloud Run Deployment")
    print(f"Project ID: {args.project_id}")
    print(f"Region: {args.region}")
    
    # Check prerequisites
    check_prerequisites()
    
    # Setup project
    setup_project(args.project_id, args.region)
    
    if not args.setup_only:
        # Build and deploy
        build_and_deploy(args.project_id, args.region, not args.local_build)
        
        # Get service URL
        service_url = get_service_url(args.project_id, args.region)
        print(f"\n🎉 Deployment completed!")
        print(f"Service URL: {service_url}")
        
        # Test deployment
        if not args.skip_test:
            test_deployment(service_url)
        
        print(f"\n📋 Next steps:")
        print(f"1. Set up environment variables (API keys) in Cloud Run console")
        print(f"2. Configure custom domain if needed")
        print(f"3. Set up monitoring and logging")
        print(f"4. Test the API endpoints:")
        print(f"   - Health: {service_url}/health")
        print(f"   - Agent Info: {service_url}/agent/info")
        print(f"   - Chat: POST {service_url}/chat")


if __name__ == "__main__":
    main()