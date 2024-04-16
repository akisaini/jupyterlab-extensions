import { Application } from '@lumino/application';
import { DOMWidgetView } from '@jupyter-widgets/base';
import { Widget } from '@lumino/widgets';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';
import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { PageConfig } from '@jupyterlab/coreutils';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { store } from '@labshare/polus-render';
import { RenderModel } from './widget';
import { MODULE_NAME, MODULE_VERSION } from './version';
import { Dropzone } from './Dropzone'; 
import { Drag } from '@lumino/dragdrop';
import * as ReactDOM from 'react-dom';
import React from 'react';


declare global {
  namespace JSX {
    interface IntrinsicElements {
      'polus-render': any; // Define 'polus-render' as any type
    }
  }
}


const EXTENSION_ID = 'jupyterlab_polus_render:plugin';


// Get the base URL of the JupyterLab session
const baseUrl = PageConfig.getBaseUrl();
// URL for serving images
const renderFilePrefix = 'jupyterlab-polus-render/image'

/**
 * The render plugin.
 */
const renderPlugin:  JupyterFrontEndPlugin<void> = {
  id: EXTENSION_ID,
  requires: [
    IJupyterWidgetRegistry,
    IFileBrowserFactory
  ],
  activate: activateWidgetExtension,
  autoStart: true,
}

export default renderPlugin;

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  app: Application<Widget>,
  registry: IJupyterWidgetRegistry,
  browserFactory: IFileBrowserFactory
): void { 
  //let path: string; // Declare path variable in the outer scope to make available in ReactDOM if needed
  const RenderView = class extends DOMWidgetView {
    loadsetState(){
      let imagePath = this.model.get('imagePath');
      let overlayPath = this.model.get('overlayPath');
      let isImagePathUrl = this.model.get('is_imagePath_url');
      let isOverlayPathUrl = this.model.get('is_overlayPath_url');
      let imageUrl = isImagePathUrl ? imagePath : `${baseUrl}${renderFilePrefix}${imagePath}`; // T/F condition ? valueIfTrue : valueIfFalse
      let overlayUrl = isOverlayPathUrl ? overlayPath : `${baseUrl}${renderFilePrefix}${overlayPath}`;
      
      // Updates the state based on current value
      this.model.set('is_imagePath_url', imagePath.startsWith('http')); 
      this.model.set('isOverlayPathUrl', overlayPath.startsWith('http')); 
      this.model.save_changes();


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

    }

    render() {
      this.loadsetState();

      // Observe any changes to imagePath and rerun the widget when it changes
      this.model.on('change:imagePath', () => {
        this.loadsetState(); // Updates the value of imagePath
        this.render(); // Re-render widgets view with new state
      }, this);

      // Observe any changes to overlayPath and rerun the widget when it changes
      this.model.on('change:overlayPath', () => {
        this.loadsetState(); // Updates the value of overlayPath
        this.render(); // Re-render widgets view with new state
      }, this);

      const { tracker }  = browserFactory;

      const handleDrop = async (e: Drag.Event): Promise<void> => {
        // Log the dropped item's data
        console.log("Item dropped:", e);
        const widget = tracker.currentWidget;
        if (!widget) {
          return;
        }
        const selectedItem = widget.selectedItems().next().value;
        if (!selectedItem) {
          return;
        }
        const relativePath = encodeURI(selectedItem.path);

        let notebook_absdir = this.model.get('notebook_absdir'); // Fetch from render.py

        // An overlay gets dropped on an image
        if (relativePath.endsWith('.json')){
          if (filePath) {
            filePath.innerHTML = `Path: ${relativePath}`;
          }
          this.model.set('overlayPath', notebook_absdir + '/../' + relativePath);
          this.model.set('is_overlayPath_url', false);
          this.model.save_changes();

          this.loadsetState(); 
        }
        // An image gets dropped
        else {
          //console.log(relativePath)
          if (filePath) {
            filePath.innerHTML = `Path: ${relativePath}`; 
          }
          this.model.set('imagePath', notebook_absdir + '/../' + relativePath);
          this.model.set('is_imagePath_url', false);
          this.model.save_changes();

          this.loadsetState();
        }
        
      };

      this.el.innerHTML = `
      <div id="filePath"></div>
      <div id="dropzoneContainer"></div>
      `;

      // Create the container element
      const dropzoneContainer = this.el.querySelector('#dropzoneContainer');
      const filePath = this.el.querySelector('#filePath'); 

      // Render the Dropzone component inside the container
      ReactDOM.render(
        <Dropzone onDrop={handleDrop}>
          <div style={{ width: '100%', height: '900px' }}>
            {/* Polus-render element  */}
            <polus-render></polus-render>
          </div>
        </Dropzone>,
        dropzoneContainer
      );
    }
  } 

  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: {
      RenderModel,
      RenderView
    },
  });
}