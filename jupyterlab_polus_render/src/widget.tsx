// coding: utf-8

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { Context } from '@jupyterlab/docregistry';

import { MODULE_NAME, MODULE_VERSION } from './version';
import { PageConfig } from '@jupyterlab/coreutils';
import { store } from '@labshare/polus-render';
import { Dropzone } from './Dropzone'; 
import { IDragEvent } from '@lumino/dragdrop';
import * as ReactDOM from 'react-dom';
import React, { useRef } from 'react';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { PathExt } from '@jupyterlab/coreutils';

// Import the CSS
import '../css/widget.css';



// Get the base URL of the JupyterLab session
const baseUrl = PageConfig.getBaseUrl();
// URL for serving images
const renderFilePrefix = 'jupyterlab-polus-render/image'

export class RenderModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: RenderModel.model_name,
      _model_module: RenderModel.model_module,
      _model_module_version: RenderModel.model_module_version,
      _view_name: RenderModel.view_name,
      _view_module: RenderModel.view_module,
      _view_module_version: RenderModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'RenderModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'RenderView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class RenderView extends DOMWidgetView {
    private browserFactory: IFileBrowserFactory;
    private context: Context;

    async fileBrowser(browserFactory: IFileBrowserFactory): Promise<void> {
    this.browserFactory = browserFactory;
    // Create file browser instance 
    const leftPane = browserFactory.createFileBrowser('filebrowser');
    // Activate the file browser and wait
    leftPane.activate();
    // Wait for one sec
    await new Promise(resolve => setTimeout(resolve, 1000));
    // Get the refreshed signal from the file browser model regarding the selected file
    const selectedItems = leftPane.selectedItems();
    for await (const item of selectedItems) {
      console.log('File Name:', item.name);
      console.log('File Path:', item.path);
      console.log('File Type:', item.type);
      }
    }
  
  render() {
    let imagePath = this.model.get('imagePath');
    let overlayPath = this.model.get('overlayPath');
    let isImagePathUrl = this.model.get('is_imagePath_url');
    let isOverlayPathUrl = this.model.get('is_overlayPath_url');
    let imageUrl = isImagePathUrl ? imagePath : `${baseUrl}${renderFilePrefix}${imagePath}`; // T/F condition ? valueIfTrue : valueIfFalse
    let overlayUrl = isOverlayPathUrl ? overlayPath : `${baseUrl}${renderFilePrefix}${overlayPath}`;
    
    // Set the image url
    store.setState({
      urls: [
        imageUrl,
      ],
    });

    // Set the overlay url
    fetch(overlayUrl).then((response) => {
      response.json().then((overlayData) => {
        store.setState({
          overlayData,
        });
        const heatmapIds = Object.keys(overlayData.value_range)
          .map((d: any) => ({ label: d, value: d }))
          .concat({ label: 'None', value: null });
    
        store.setState({
          heatmapIds,
        });
      });
    });    
    
    
  
    this.el.innerHTML = `
      <div id="fileInfo"></div>
      <div id="dropzoneContainer"></div>
    `;
    
    

    const handleDrop = async (e: IDragEvent): Promise<void> => {
      // Log the dropped item's data
      console.log("Item dropped:", e);

      const contextRef = useRef(this.context);
      console.log(contextRef.current.path);
      console.log(PathExt.dirname);
      console.log(PathExt.dirname(contextRef.current.path));
      // // HTML data transfer to capture file
      // const droppedFile = e.dataTransfer?.files[0].name;
      // console.log(droppedFile);
      // const fileInfoDiv = document.getElementById('fileInfo');
      // if (fileInfoDiv) {
      //   fileInfoDiv.innerText = `File Name: ${droppedFile}, and the full path is ${imageUrl}/${droppedFile}`;
      // } OR
      // const droppedFiles = e.dataTransfer?.files;
      // if (droppedFiles) {
      //     // Process each dropped file
      //     for (let i = 0; i < droppedFiles.length; i++) {
      //         const file = droppedFiles[i];
      //         console.log('Dropped file:', file.name, file.type, file.size);
      //     }
      // }

      if (this.browserFactory) {
        await this.fileBrowser(this.browserFactory);
      }
    };

    // Get the container element
    const dropzoneContainer = this.el.querySelector('#dropzoneContainer');

    // Render the Dropzone component inside the container
    ReactDOM.render(
      <Dropzone onDrop={handleDrop}>
        <div style={{ width: '100%', height: '900px' }}></div>
      </Dropzone>,
      dropzoneContainer
    );
      
  }
}
    
