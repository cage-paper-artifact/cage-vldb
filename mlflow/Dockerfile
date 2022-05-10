FROM continuumio/miniconda3:4.9.2

# The model to copy into the container
ARG MODELNAME

# Create the environment using conda
RUN conda install -c conda-forge mlflow=1.20.2
RUN conda install -c anaconda scikit-learn=0.23.1
RUN conda install -c anaconda cloudpickle==1.6.0

# '/workdir/' is base directory
WORKDIR /workdir/

# Copy the model folder into the container
COPY $MODELNAME /workdir/model

# Create the local conda env
RUN mlflow models prepare-env -m /workdir/model/ 

# Expose mlflow port
EXPOSE 5001

# Start the model serving.
CMD [ "mlflow", "models", "serve", "-m", "/workdir/model", "-p", "5001" , "-h", "0.0.0.0" ]
